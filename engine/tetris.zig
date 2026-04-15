const std = @import("std");

pub const Tetromino = enum { i, o, t, l, j, s, z };
pub const move_count: [7]usize = .{ 17, 9, 34, 34, 34, 17, 17 };
pub const BoardState = [10]u20;

pub fn printBoardDebug(board: BoardState) void {
    var j: u5 = 0;
    while (j < 20) : (j += 1) {
        for (0..10) |i| {
            const bit = (board[i] >> j) & 1;
            const c: u8 = if (bit == 0) '.' else '#';
            std.debug.print("{c}", .{c});
        }
        std.debug.print("\n", .{});
    }
}

pub fn parseBoardDebug(str: []const u8) BoardState {
    var board: BoardState = .{0} ** 10;
    var iter = std.mem.splitScalar(u8, str, '\n');
    var j: u5 = 0;
    while (iter.next()) |line| {
        for (line, 0..) |c, i| {
            const bit: u20 = if (c == '#') 1 else 0;
            board[i] |= (bit << j);
        }
        j += 1;
    }
    return board;
}

pub inline fn makeMove(
    board: BoardState,
    tet: Tetromino,
    move: u8,
    cleared: *u8,
) ?BoardState {
    const new_board = switch (tet) {
        .i => makeMoveI(board, move),
        .o => makeMoveO(board, move),
        .t => makeMoveT(board, move),
        .l => makeMoveL(board, move),
        .j => makeMoveJ(board, move),
        .s => makeMoveS(board, move),
        .z => makeMoveZ(board, move),
    } orelse return null;
    return clearRows(new_board, cleared);
}

const _15: u20 = 15;
const _1: u20 = 1;
const _3: u20 = 3;
const _7: u20 = 7;

inline fn makeMoveI(
    board: BoardState,
    move: u8,
) ?BoardState {
    var new_board: BoardState = board;
    if (move < 10) {
        const space = @ctz(board[move]);
        if (space < 4) return null;
        new_board[move] |= (_15 << (space - 4));
        return new_board;
    }
    var space: u5 = 20;
    for (move - 10..move - 6) |i| {
        const new_space = @ctz(new_board[i]);
        if (new_space < space) {
            space = new_space;
        }
    }
    if (space == 0) return null;
    for (move - 10..move - 6) |i| {
        new_board[i] |= (_1 << (space - 1));
    }
    return new_board;
}

inline fn makeMoveO(
    board: BoardState,
    move: u8,
) ?BoardState {
    const space1 = @ctz(board[move]);
    const space2 = @ctz(board[move + 1]);
    var space = space1;
    if (space2 < space) space = space2;
    if (space < 2) return null;
    var new_board: BoardState = board;
    new_board[move] |= (_3 << (space - 2));
    new_board[move + 1] |= (_3 << (space - 2));
    return new_board;
}

inline fn makeMoveT(
    board: BoardState,
    move: u8,
) ?BoardState {
    var new_board: BoardState = board;
    if (move < 8) {
        const space1 = @ctz(board[move]);
        const space2 = @ctz(board[move + 1]);
        const space3 = @ctz(board[move + 2]);
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move] |= (_1 << (space - 1));
        new_board[move + 1] |= (_3 << (space - 2));
        new_board[move + 2] |= (_1 << (space - 1));
        return new_board;
    }
    if (move < 16) {
        const space1 = @ctz(board[move - 8]) + 1;
        const space2 = @ctz(board[move - 7]);
        const space3 = @ctz(board[move - 6]) + 1;
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move - 8] |= (_1 << (space - 2));
        new_board[move - 7] |= (_3 << (space - 2));
        new_board[move - 6] |= (_1 << (space - 2));
        return new_board;
    }
    if (move < 25) {
        const space1 = @ctz(board[move - 16]);
        const space2 = @ctz(board[move - 15]) + 1;
        var space = space1;
        if (space2 < space) space = space2;
        if (space < 3) return null;
        new_board[move - 16] |= (_7 << (space - 3));
        new_board[move - 15] |= (_1 << (space - 2));
        return new_board;
    }
    const space1 = @ctz(board[move - 25]) + 1;
    const space2 = @ctz(board[move - 24]);
    var space = space1;
    if (space2 < space) space = space2;
    if (space < 3) return null;
    new_board[move - 25] |= (_1 << (space - 2));
    new_board[move - 24] |= (_7 << (space - 3));
    return new_board;
}

inline fn makeMoveJ(
    board: BoardState,
    move: u8,
) ?BoardState {
    var new_board: BoardState = board;
    if (move < 8) {
        const space1 = @ctz(board[move]);
        const space2 = @ctz(board[move + 1]);
        const space3 = @ctz(board[move + 2]);
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move] |= (_3 << (space - 2));
        new_board[move + 1] |= (_1 << (space - 1));
        new_board[move + 2] |= (_1 << (space - 1));
        return new_board;
    }
    if (move < 16) {
        const space1 = @ctz(board[move - 8]) + 1;
        const space2 = @ctz(board[move - 7]) + 1;
        const space3 = @ctz(board[move - 6]);
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move - 8] |= (_1 << (space - 2));
        new_board[move - 7] |= (_1 << (space - 2));
        new_board[move - 6] |= (_3 << (space - 2));
        return new_board;
    }
    if (move < 25) {
        const space1 = @ctz(board[move - 16]);
        const space2 = @ctz(board[move - 15]);
        var space = space1;
        if (space2 < space) space = space2;
        if (space < 3) return null;
        new_board[move - 16] |= (_1 << (space - 1));
        new_board[move - 15] |= (_7 << (space - 3));
        return new_board;
    }
    const space1 = @ctz(board[move - 25]);
    const space2 = @ctz(board[move - 24]) + 2;
    var space = space1;
    if (space2 < space) space = space2;
    if (space < 3) return null;
    new_board[move - 25] |= (_7 << (space - 3));
    new_board[move - 24] |= (_1 << (space - 3));
    return new_board;
}

inline fn makeMoveL(
    board: BoardState,
    move: u8,
) ?BoardState {
    var new_board: BoardState = board;
    if (move < 8) {
        const space1 = @ctz(board[move]);
        const space2 = @ctz(board[move + 1]);
        const space3 = @ctz(board[move + 2]);
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move] |= (_1 << (space - 1));
        new_board[move + 1] |= (_1 << (space - 1));
        new_board[move + 2] |= (_3 << (space - 2));
        return new_board;
    }
    if (move < 16) {
        const space1 = @ctz(board[move - 8]);
        const space2 = @ctz(board[move - 7]) + 1;
        const space3 = @ctz(board[move - 6]) + 1;
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move - 8] |= (_3 << (space - 2));
        new_board[move - 7] |= (_1 << (space - 2));
        new_board[move - 6] |= (_1 << (space - 2));
        return new_board;
    }
    if (move < 25) {
        const space1 = @ctz(board[move - 16]);
        const space2 = @ctz(board[move - 15]);
        var space = space1;
        if (space2 < space) space = space2;
        if (space < 3) return null;
        new_board[move - 16] |= (_7 << (space - 3));
        new_board[move - 15] |= (_1 << (space - 1));
        return new_board;
    }
    const space1 = @ctz(board[move - 25]) + 2;
    const space2 = @ctz(board[move - 24]);
    var space = space1;
    if (space2 < space) space = space2;
    if (space < 3) return null;
    new_board[move - 25] |= (_1 << (space - 3));
    new_board[move - 24] |= (_7 << (space - 3));
    return new_board;
}

inline fn makeMoveS(
    board: BoardState,
    move: u8,
) ?BoardState {
    var new_board: BoardState = board;
    if (move < 8) {
        const space1 = @ctz(board[move]);
        const space2 = @ctz(board[move + 1]);
        const space3 = @ctz(board[move + 2]) + 1;
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move] |= (_1 << (space - 1));
        new_board[move + 1] |= (_3 << (space - 2));
        new_board[move + 2] |= (_1 << (space - 2));
        return new_board;
    }
    const space1 = @ctz(board[move - 8]) + 1;
    const space2 = @ctz(board[move - 7]);
    var space = space1;
    if (space2 < space) space = space2;
    if (space < 3) return null;
    new_board[move - 8] |= (_3 << (space - 3));
    new_board[move - 7] |= (_3 << (space - 2));
    return new_board;
}

inline fn makeMoveZ(
    board: BoardState,
    move: u8,
) ?BoardState {
    var new_board: BoardState = board;
    if (move < 8) {
        const space1 = @ctz(board[move]) + 1;
        const space2 = @ctz(board[move + 1]);
        const space3 = @ctz(board[move + 2]);
        var space = space1;
        if (space2 < space) space = space2;
        if (space3 < space) space = space3;
        if (space < 2) return null;
        new_board[move] |= (_1 << (space - 2));
        new_board[move + 1] |= (_3 << (space - 2));
        new_board[move + 2] |= (_1 << (space - 1));
        return new_board;
    }
    const space1 = @ctz(board[move - 8]);
    const space2 = @ctz(board[move - 7]) + 1;
    var space = space1;
    if (space2 < space) space = space2;
    if (space < 3) return null;
    new_board[move - 8] |= (_3 << (space - 2));
    new_board[move - 7] |= (_3 << (space - 3));
    return new_board;
}

pub inline fn clearRows(board: BoardState, cleared: *u8) BoardState {
    comptime var masks: [21]u20 = undefined;
    comptime {
        for (0..21) |i| {
            masks[i] = (1 << i) - 1;
        }
    }

    var full_rows: u20 = std.math.maxInt(u20);
    for (board) |col| full_rows &= col;

    const l_size = @clz(full_rows);
    const r_size = @ctz(full_rows);
    if (l_size == 20) {
        cleared.* = 0;
        return board;
    }
    const l_mask = ~masks[20 - l_size];
    const r_mask = masks[r_size];
    const center = (full_rows & (~l_mask)) >> r_size;
    const c_mask: u20, const shift1: u5, const shift2: u5 = switch (center) {
        1 => .{ 0, 0, 1 },
        3 => .{ 0, 0, 2 },
        5 => .{ _1 << (r_size + 1), 1, 2 },
        7 => .{ 0, 0, 3 },
        9 => .{ _3 << (r_size + 1), 1, 2 },
        11 => .{ _1 << (r_size + 2), 1, 3 },
        13 => .{ _1 << (r_size + 1), 2, 3 },
        15 => .{ 0, 0, 4 },
        else => unreachable,
    };
    cleared.* = shift2;

    var new_board: BoardState = undefined;
    for (board, &new_board) |col, *new_col| {
        new_col.* = (col & l_mask) | ((col & c_mask) << shift1) | ((col & r_mask) << shift2);
    }
    return new_board;
}

pub fn random_piece(rand: std.Random) Tetromino {
    return @enumFromInt(rand.intRangeLessThan(usize, 0, 7));
}

pub fn pieceFromChar(c: u8) ?Tetromino {
    return switch (c) {
        'y' => .o,
        'b' => .j,
        'r' => .z,
        'g' => .s,
        'o' => .l,
        'm' => .t,
        'c' => .i,
        else => null,
    };
}
