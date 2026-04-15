const std = @import("std");
const tetris = @import("tetris.zig");

pub fn main() !void {
    var engine: EngineState = .{
        .pieces = undefined,
        .layers = undefined,
        .current_layer = 0,
    };
    var board: Board = .{
        .state = undefined,
        .holding = undefined,
        .lines_cleared = 0,
    };

    var stdin_buf: [1024]u8 = undefined;
    var stdin_reader = std.fs.File.stdin().reader(&stdin_buf);
    const stdin = &stdin_reader.interface;

    var stdout_buf: [1024]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buf);
    const stdout = &stdout_writer.interface;

    main: while (true) {
        const message = (try stdin.takeDelimiter('\n')).?;
        const board_msg = message[0..200];
        const pieces = message[200..206];
        const hold = message[206];

        board.state = .{0} ** 10;
        for (board_msg, 0..) |c, idx| {
            const i = idx % 10;
            const j = idx / 10;
            const bit: u20 = if (c == '_') 0 else 1;
            board.state[i] |= (bit << @intCast(j));
        }
        board.holding = tetris.pieceFromChar(hold);
        for (pieces, 0..) |c, i| {
            engine.pieces[i] = tetris.pieceFromChar(c) orelse {
                print_retry(stdout, "\n", .{});
                continue :main;
            };
        }

        const eval = evaluate(&engine, board);
        if (eval) |e| {
            var response_buf: [64]u8 = undefined;
            const response = make_move_str(&response_buf, engine.pieces[0], board.holding, e.best_move);
            print_retry(stdout, "{s}\n", .{response});
        } else {
            print_retry(stdout, "v\n", .{});
        }
    }
}

fn print_retry(writer: *std.Io.Writer, comptime fmt: []const u8, args: anytype) void {
    while (true) {
        writer.print(fmt, args) catch {
            std.Thread.sleep(std.time.ns_per_ms * 50);
            continue;
        };
        break;
    }
    while (true) {
        writer.flush() catch {
            std.Thread.sleep(std.time.ns_per_ms * 50);
            continue;
        };
        break;
    }
}

const Board = struct {
    state: tetris.BoardState,
    holding: ?tetris.Tetromino,
    lines_cleared: u8,
};

const Layer = struct {
    boards: [34]?Board,
    candidate_buf: [34]usize,
    candidates: []usize,
    current_candidate: usize,
};

const EngineState = struct {
    pieces: [6]tetris.Tetromino,
    layers: [6]Layer,
    current_layer: usize,
};

const Move = struct {
    swap: bool,
    id: u8,
};

const Eval = struct {
    best_move: Move,
    eval: i64,
};

const tetris_bonus: i64 = 100;

fn evaluate(engine: *EngineState, current_board: Board) ?Eval {
    const layer_id = engine.current_layer;
    const layer: *Layer = &engine.layers[layer_id];
    const piece = engine.pieces[engine.current_layer];
    const moves = tetris.move_count[@intFromEnum(piece)];

    if (piece == .i or current_board.holding == .i) i: {
        var new_board: Board = undefined;
        var tetris_move: ?u8 = null;
        for (0..10) |move| {
            new_board.state = tetris.makeMove(
                current_board.state,
                .i,
                @intCast(move),
                &new_board.lines_cleared,
            ) orelse continue;
            if (new_board.lines_cleared == 4) {
                tetris_move = @intCast(move);
                break;
            }
        }
        if (tetris_move) |tm| {
            new_board.holding = blk: {
                if (piece == .i) {
                    break :blk current_board.holding;
                }
                break :blk piece;
            };
            engine.current_layer += 1;
            defer engine.current_layer -= 1;
            const eval: i64 = blk: {
                if (layer_id == 5) {
                    break :blk heuristic(new_board.state) + tetris_bonus + new_board.lines_cleared;
                }

                break :blk evaluate(engine, new_board).?.eval + new_board.lines_cleared;
            };
            return .{
                .best_move = .{
                    .id = tm,
                    .swap = piece != .i,
                },
                .eval = eval,
            };
        }
        if (current_board.holding != .i) {
            new_board.holding = .i;
            new_board.lines_cleared = 0;
            new_board.state = current_board.state;
            engine.current_layer += 1;
            defer engine.current_layer -= 1;
            const eval: i64 = blk: {
                if (layer_id == 5) {
                    break :blk heuristic(new_board.state);
                }
                const e = evaluate(engine, new_board);
                if (e == null) break :i;
                break :blk e.?.eval;
            };
            return .{
                .best_move = .{
                    .id = 34,
                    .swap = true,
                },
                .eval = eval,
            };
        }
    }

    for (0..moves) |move| {
        const board: *?Board = &layer.boards[move];
        var new_board: Board = undefined;
        const boardState = tetris.makeMove(
            current_board.state,
            piece,
            @intCast(move),
            &new_board.lines_cleared,
        );
        if (boardState) |bs| {
            new_board.state = bs;
            board.* = new_board;
        } else {
            board.* = null;
        }
    }

    {
        var i: usize = 0;
        for (0..moves) |move| {
            if (layer.boards[move] != null) {
                layer.candidate_buf[i] = move;
                i += 1;
            }
        }
        layer.candidates = layer.candidate_buf[0..i];
    }

    var heuristics_buf: [34]i64 = undefined;
    for (layer.candidates, 0..) |candidate, i| {
        heuristics_buf[i] = heuristic(layer.boards[candidate].?.state);
    }
    const heuristics = heuristics_buf[0..layer.candidates.len];

    const cand_limit = 4;
    if (layer.candidates.len > cand_limit) {
        for (cand_limit..layer.candidates.len) |i| {
            for (0..cand_limit) |j| {
                if (heuristics[i] > heuristics[j]) {
                    const temp = layer.candidates[j];
                    layer.candidates[j] = layer.candidates[i];
                    layer.candidates[i] = temp;
                    const temp_h = heuristics[j];
                    heuristics[j] = heuristics[i];
                    heuristics[i] = temp_h;
                }
            }
        }
        layer.candidates = layer.candidates[0..cand_limit];
    }

    var best_eval: ?Eval = null;
    engine.current_layer += 1;
    defer engine.current_layer -= 1;
    for (layer.candidates) |candidate| {
        const board = layer.boards[candidate].?;
        const eval: i64 = blk: {
            if (layer_id == 5) {
                break :blk heuristic(board.state) + board.lines_cleared;
            }
            const e = evaluate(engine, board);
            if (e == null) continue;
            break :blk e.?.eval;
        };
        if (best_eval == null or eval > best_eval.?.eval) {
            best_eval = Eval{
                .eval = eval,
                .best_move = .{
                    .id = @intCast(candidate),
                    .swap = false,
                },
            };
        }
    }
    return best_eval;
}

fn heuristic(board: tetris.BoardState) i64 {
    var cols: u20 = 0;
    var holes: u32 = 0;
    var min_tetris_space: u5 = 20;
    var prev_col: ?u20 = null;
    var bumpiness: u32 = 0;
    for (board) |col| {
        if (prev_col) |p_col| {
            const a = @ctz(col);
            const b = @ctz(p_col);
            bumpiness += if (a > b) a - b else b - a;
        }
        prev_col = col;
        cols |= col;
        holes += 20 - @popCount(col) - @ctz(col);
        const shift = @ctz(col);
        const tetris_space = if (shift < 20) @ctz(~(col >> shift)) + shift else 20;
        if (tetris_space < min_tetris_space) {
            min_tetris_space = tetris_space;
        }
    }
    const min_space = if (@ctz(cols) < 7) @ctz(cols) else 7;

    const tetris_potential = blk: {
        if (min_tetris_space < 4) break :blk 0;
        var tetris_unfilled_cells: u8 = 0;
        for (board) |col| {
            const floor: u20 = if (min_tetris_space > 4) @as(u20, 1) << (24 - min_tetris_space) else 0;
            tetris_unfilled_cells += @ctz((col >> (min_tetris_space - 4)) | floor);
        }
        break :blk (60 -| tetris_unfilled_cells);
    };

    var result: i64 = tetris_potential;
    result += 10 * @as(i64, min_space);
    result -= 4 * holes;
    result -= bumpiness;
    return result;
}

const move_strings: [7][]const []const u8 = .{
    &.{
        "l<<<<",
        "l<<<",
        "l<<",
        "l<",
        "l",
        "l>",
        "l>>",
        "l>>>",
        "l>>>>",
        "l>>>>>",
        "<<<",
        "<<",
        "<",
        "",
        ">",
        ">>",
        ">>>",
    },
    &.{
        "<<<<",
        "<<<",
        "<<",
        "<",
        "",
        ">",
        ">>",
        ">>>",
        ">>>>",
    },
    &.{
        "<<<",
        "<<",
        "<",
        "",
        ">",
        ">>",
        ">>>",
        ">>>>",
        "ll<<<",
        "ll<<",
        "ll<",
        "ll",
        "ll>",
        "ll>>",
        "ll>>>",
        "ll>>>>",
        "r<<<<",
        "r<<<",
        "r<<",
        "r<",
        "r",
        "r>",
        "r>>",
        "r>>>",
        "r>>>>",
        "l<<<",
        "l<<",
        "l<",
        "l",
        "l>",
        "l>>",
        "l>>>",
        "l>>>>",
        "l>>>>>",
    },
    &.{
        "<<<",
        "<<",
        "<",
        "",
        ">",
        ">>",
        ">>>",
        ">>>>",
        "ll<<<",
        "ll<<",
        "ll<",
        "ll",
        "ll>",
        "ll>>",
        "ll>>>",
        "ll>>>>",
        "r<<<<",
        "r<<<",
        "r<<",
        "r<",
        "r",
        "r>",
        "r>>",
        "r>>>",
        "r>>>>",
        "l<<<",
        "l<<",
        "l<",
        "l",
        "l>",
        "l>>",
        "l>>>",
        "l>>>>",
        "l>>>>>",
    },
    &.{
        "<<<",
        "<<",
        "<",
        "",
        ">",
        ">>",
        ">>>",
        ">>>>",
        "ll<<<",
        "ll<<",
        "ll<",
        "ll",
        "ll>",
        "ll>>",
        "ll>>>",
        "ll>>>>",
        "l<<<",
        "l<<",
        "l<",
        "l",
        "l>",
        "l>>",
        "l>>>",
        "l>>>>",
        "l>>>>>",
        "r<<<<",
        "r<<<",
        "r<<",
        "r<",
        "r",
        "r>",
        "r>>",
        "r>>>",
        "r>>>>",
    },
    &.{
        "<<<",
        "<<",
        "<",
        "",
        ">",
        ">>",
        ">>>",
        ">>>>",
        "r<<<<",
        "r<<<",
        "r<<",
        "r<",
        "r",
        "r>",
        "r>>",
        "r>>>",
        "r>>>>",
    },
    &.{
        "<<<",
        "<<",
        "<",
        "",
        ">",
        ">>",
        ">>>",
        ">>>>",
        "r<<<<",
        "r<<<",
        "r<<",
        "r<",
        "r",
        "r>",
        "r>>",
        "r>>>",
        "r>>>>",
    },
};

fn make_move_str(buf: []u8, main_piece: tetris.Tetromino, holding: ?tetris.Tetromino, move: Move) []u8 {
    var i: usize = 0;
    var piece: ?tetris.Tetromino = main_piece;
    if (move.swap) {
        buf[i] = 'h';
        i += 1;
        piece = holding;
    }
    if (move.id == 34) return buf[0..i];
    const move_str = move_strings[@intFromEnum(piece.?)][move.id];
    @memcpy(buf[i .. i + move_str.len], move_str);
    i += move_str.len;
    buf[i] = 'v';
    i += 1;
    return buf[0..i];
}
