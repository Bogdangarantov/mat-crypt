import numpy as np
from .State import State


def omegaJV(j, v):
    return [(j << 4) ^ v] + [0x00] * 7


def KLV(v, X: State):
    X = State(np.copy(X))
    for col_id in range(len(X[0])):
        vec = omegaJV(col_id, v)
        X.addColumnMod(vec, col_id, 2)
    return X


class KupynaRealization:

    def __init__(self, hash_size=256):
        self.I, self.t, self.c = self._size(hash_size)
        self.IV = b"\x04" + b"\x00" * (self.I // 8 - 1)
        self.G = self.converterBytes(self.IV)
        self.n = hash_size // 8
        self.N = hash_size
        self.pi0 = (0xAB, 0x43, 0x5F, 0x06, 0x6B, 0x75, 0x6E, 0x59, 0x71, 0xDF, 0x87, 0x95, 0x17, 0xF0, 0xDB, 0x09,
                    0x6D, 0xF3, 0x1D, 0xCB, 0xC9, 0x4D, 0x2C, 0xAF, 0x79, 0xE0, 0x97, 0xFD, 0x6F, 0x4B, 0x45, 0x39,
                    0x3E, 0xDD, 0xA3, 0x4F, 0xB4, 0xB6, 0x9A, 0x0E, 0x1F, 0xBF, 0x15, 0xE1, 0x49, 0xD2, 0x93, 0xC6,
                    0x92, 0x72, 0x9E, 0x61, 0xD1, 0x63, 0xFA, 0xEE, 0xF4, 0x19, 0xD5, 0xAD, 0x58, 0xA4, 0xBB, 0xA1,
                    0xDC, 0xF2, 0x83, 0x37, 0x42, 0xE4, 0x7A, 0x32, 0x9C, 0xEC, 0xAB, 0x4A, 0xBF, 0x6E, 0x04, 0x27,
                    0x2E, 0xE7, 0xE2, 0x5A, 0x96, 0x16, 0x23, 0x2B, 0xC2, 0x65, 0x66, 0x0F, 0xBC, 0xA9, 0x47, 0x41,
                    0x34, 0x48, 0xFC, 0xB7, 0x6A, 0x88, 0xA5, 0x53, 0x86, 0xF9, 0x5B, 0xDB, 0x38, 0x7B, 0xC3, 0x1E,
                    0x22, 0x33, 0x24, 0x28, 0x36, 0xC7, 0xB2, 0x3B, 0xBE, 0x77, 0xBA, 0xF5, 0x14, 0x9F, 0x08, 0x55,
                    0x9B, 0x4C, 0xFE, 0x60, 0x5C, 0xDA, 0x18, 0x46, 0xCD, 0x7D, 0x21, 0xB0, 0x3F, 0x1B, 0x89, 0xFF,
                    0xEB, 0x84, 0x69, 0x3A, 0x9D, 0xD7, 0xD3, 0x70, 0x67, 0x40, 0xB5, 0xDE, 0x5D, 0x30, 0x91, 0xB1,
                    0x78, 0x11, 0x01, 0xE5, 0x00, 0x68, 0x98, 0xA0, 0xC5, 0x02, 0xA6, 0x74, 0x2D, 0x0B, 0xA2, 0x76,
                    0xB3, 0xBE, 0xCE, 0xBD, 0xAE, 0xE9, 0xBA, 0x31, 0x1C, 0xEC, 0xF1, 0x99, 0x94, 0xAA, 0xF6, 0x26,
                    0x2F, 0xEF, 0xEB, 0xBC, 0x35, 0x03, 0xD4, 0x7F, 0xFB, 0x05, 0xC1, 0x5E, 0x90, 0x20, 0x3D, 0x82,
                    0xF7, 0xEA, 0x0A, 0x0D, 0x7E, 0xF5, 0x50, 0x1A, 0xC4, 0x07, 0x57, 0xBB, 0x3C, 0x62, 0xE3, 0xCB,
                    0xAC, 0x52, 0x64, 0x10, 0xD0, 0xD9, 0x13, 0x0C, 0x12, 0x29, 0x51, 0xB9, 0xCF, 0xD6, 0x73, 0x8D,
                    0x81, 0x54, 0xC0, 0xED, 0x4E, 0x44, 0xA7, 0x2A, 0x85, 0x25, 0xE6, 0xCA, 0x7C, 0xBB, 0x56, 0x80)
        self.pi1 = (0xCE, 0xBB, 0xEB, 0x92, 0xEA, 0xCB, 0x13, 0xC1, 0xE9, 0x3A, 0xD6, 0xB2, 0xD2, 0x90, 0x17, 0xFB,
                    0x42, 0x15, 0x56, 0xB4, 0x65, 0x1C, 0x88, 0x43, 0xC5, 0x5C, 0x36, 0xBA, 0xF5, 0x57, 0x67, 0x8D,
                    0x31, 0xF6, 0x64, 0x58, 0x9E, 0xF4, 0x22, 0xAA, 0x75, 0x0F, 0x02, 0xB1, 0xDF, 0x6D, 0x73, 0x4D,
                    0x7C, 0x26, 0x2E, 0xF7, 0x08, 0x5D, 0x44, 0x3E, 0x9F, 0x14, 0xCB, 0xAE, 0x54, 0x10, 0xD5, 0xBC,
                    0x1A, 0x6B, 0x69, 0xF3, 0xBD, 0x33, 0xAB, 0xFA, 0xD1, 0x9B, 0x68, 0x4E, 0x16, 0x95, 0x91, 0xEE,
                    0x4C, 0x63, 0xBE, 0x5B, 0xEC, 0x3C, 0x19, 0xA1, 0x81, 0x49, 0x7B, 0xD9, 0x6F, 0x37, 0x60, 0xCA,
                    0xE7, 0x2B, 0x48, 0xFD, 0x96, 0x45, 0xFC, 0x41, 0x12, 0x0D, 0x79, 0xE5, 0x89, 0xBC, 0xE3, 0x20,
                    0x30, 0xDC, 0xB7, 0x6E, 0x4A, 0xB5, 0x3F, 0x97, 0xD4, 0x62, 0x2D, 0x06, 0xA4, 0xA5, 0x83, 0x5F,
                    0x2A, 0xDA, 0xC9, 0x00, 0x7E, 0xA2, 0x55, 0xBF, 0x11, 0xD5, 0x9C, 0xCF, 0x0E, 0x0A, 0x3D, 0x51,
                    0x7D, 0x93, 0x1B, 0xFE, 0xC4, 0x47, 0x09, 0x86, 0x0B, 0x5F, 0x9D, 0x6A, 0x07, 0xB9, 0xB0, 0x98,
                    0x18, 0x32, 0x71, 0x4B, 0xEF, 0x3B, 0x70, 0xA0, 0xE4, 0x40, 0xFF, 0xC3, 0xA9, 0xE6, 0x78, 0xF9,
                    0xBB, 0x46, 0x80, 0x1E, 0x38, 0xE1, 0xBB, 0xAB, 0xE0, 0x0C, 0x23, 0x76, 0x1D, 0x25, 0x24, 0x05,
                    0xF1, 0x6E, 0x94, 0x28, 0x9A, 0x84, 0xEB, 0xA3, 0x4F, 0x77, 0xD3, 0x85, 0xE2, 0x52, 0xF2, 0x82,
                    0x50, 0x7A, 0x2F, 0x74, 0x53, 0xB3, 0x61, 0xAF, 0x39, 0x35, 0xDE, 0xCD, 0x1F, 0x99, 0xAC, 0xAD,
                    0x72, 0x2C, 0xDD, 0xD0, 0x87, 0xBE, 0x5E, 0xA6, 0xEC, 0x04, 0xC6, 0x03, 0x34, 0xFB, 0xDB, 0x59,
                    0xB6, 0xC2, 0x01, 0xF0, 0x5A, 0xED, 0xA7, 0x66, 0x21, 0x7F, 0xBA, 0x27, 0xC7, 0xC0, 0x29, 0xD7)
        self.pi2 = (0x93, 0xD9, 0x9A, 0xB5, 0x98, 0x22, 0x45, 0xFC, 0xBA, 0x6A, 0xDF, 0x02, 0x9F, 0xDC, 0x51, 0x59,
                    0x4A, 0x17, 0x2B, 0xC2, 0x94, 0xF4, 0xBB, 0xA3, 0x62, 0xE4, 0x71, 0xD4, 0xCD, 0x70, 0x16, 0xE1,
                    0x49, 0x3C, 0xC0, 0xD8, 0x5C, 0x9B, 0xAD, 0x85, 0x53, 0xA1, 0x7A, 0xCB, 0x2D, 0xE0, 0xD1, 0x72,
                    0xA6, 0x2C, 0xC4, 0xE3, 0x76, 0x78, 0xB7, 0xB4, 0x09, 0x3B, 0x0E, 0x41, 0x4C, 0xDE, 0xB2, 0x90,
                    0x25, 0xA5, 0xD7, 0x03, 0x11, 0x00, 0xC3, 0x2E, 0x92, 0xEF, 0x4E, 0x12, 0x9D, 0x7D, 0xCB, 0x35,
                    0x10, 0xD5, 0x4F, 0x9E, 0x4D, 0xA9, 0x55, 0xC6, 0xD0, 0x7B, 0x18, 0x97, 0xD3, 0x36, 0xE6, 0x48,
                    0x56, 0x81, 0xBF, 0x77, 0xEC, 0x9C, 0xB9, 0xE2, 0xAC, 0xBB, 0x2F, 0x15, 0xA4, 0x7C, 0xDA, 0x38,
                    0x1E, 0x0B, 0x05, 0xD6, 0x14, 0x6E, 0x6E, 0x7E, 0x66, 0xFD, 0xB1, 0xE5, 0x60, 0xAF, 0x5E, 0x33,
                    0x87, 0xC9, 0xF0, 0x5D, 0x6D, 0x3F, 0x88, 0x8D, 0xC7, 0xF7, 0x1D, 0xE9, 0xEC, 0xED, 0x80, 0x29,
                    0x27, 0xCF, 0x99, 0xA8, 0x50, 0x0F, 0x37, 0x24, 0x28, 0x30, 0x95, 0xD2, 0x3E, 0x5B, 0x40, 0x83,
                    0xB3, 0x69, 0x57, 0x1F, 0x07, 0x1C, 0xBA, 0xBC, 0x20, 0xEB, 0xCE, 0x8E, 0xAB, 0xEE, 0x31, 0xA2,
                    0x73, 0xF9, 0xCA, 0x3A, 0x1A, 0xFB, 0x0D, 0xC1, 0xFE, 0xFA, 0xF2, 0x6F, 0xBD, 0x96, 0xDD, 0x43,
                    0x52, 0xB6, 0x08, 0xF3, 0xAE, 0xBE, 0x19, 0x89, 0x32, 0x26, 0xB0, 0xEA, 0x4B, 0x64, 0x84, 0x82,
                    0x6B, 0xF5, 0x79, 0xBF, 0x01, 0x5F, 0x75, 0x63, 0x1B, 0x23, 0x3D, 0x68, 0x2A, 0x65, 0xEB, 0x91,
                    0xF6, 0xFF, 0x13, 0x58, 0xF1, 0x47, 0x0A, 0x7F, 0xC5, 0xA7, 0xE7, 0x61, 0x5A, 0x06, 0x46, 0x44,
                    0x42, 0x04, 0xA0, 0xDB, 0x39, 0x86, 0x54, 0xAA, 0xBC, 0x34, 0x21, 0xBB, 0xFB, 0x0C, 0x74, 0x67)
        self.pi3 = (0x68, 0x8D, 0xCA, 0x4D, 0x73, 0x4B, 0x4E, 0x2A, 0xD4, 0x52, 0x26, 0xB3, 0x54, 0x1E, 0x19, 0x1F,
                    0x22, 0x03, 0x46, 0x3D, 0x2D, 0x4A, 0x53, 0x83, 0x13, 0xBA, 0xB7, 0xD5, 0x25, 0x79, 0xF5, 0xBD,
                    0x58, 0x2F, 0x0D, 0x02, 0xED, 0x51, 0x9E, 0x11, 0xF2, 0x3E, 0x55, 0x5E, 0xD1, 0x16, 0x3C, 0x66,
                    0x70, 0x5D, 0xF3, 0x45, 0x40, 0xEC, 0xE8, 0x94, 0x56, 0x08, 0xCE, 0x1A, 0x3A, 0xD2, 0xE1, 0xDF,
                    0xB5, 0x38, 0x6E, 0x0E, 0xE5, 0xF4, 0xF9, 0x86, 0xE9, 0x4F, 0xD6, 0x85, 0x23, 0xCF, 0x32, 0x99,
                    0x31, 0x14, 0xAE, 0xEE, 0xCB, 0x48, 0xD3, 0x30, 0xA1, 0x92, 0x41, 0xB1, 0x18, 0xC4, 0x2C, 0x71,
                    0x72, 0x44, 0x15, 0xFD, 0x37, 0xBE, 0x5F, 0xAA, 0x9B, 0x88, 0xDB, 0xAB, 0x89, 0x9C, 0xFA, 0x60,
                    0xEA, 0xBC, 0x62, 0x0C, 0x24, 0xA6, 0xAB, 0xEC, 0x67, 0x20, 0xDB, 0x7C, 0x28, 0xDD, 0xAC, 0x5B,
                    0x34, 0x7E, 0x10, 0xF1, 0x7B, 0x8F, 0x63, 0xA0, 0x05, 0x9A, 0x43, 0x77, 0x21, 0xBF, 0x27, 0x09,
                    0xC3, 0x9F, 0xB6, 0xD7, 0x29, 0xC2, 0xEB, 0xC0, 0xA4, 0xBB, 0xBC, 0x1D, 0xFB, 0xFF, 0xC1, 0xB2,
                    0x97, 0x2E, 0xFB, 0x65, 0xF6, 0x75, 0x07, 0x04, 0x49, 0x33, 0xE4, 0xD9, 0xB9, 0xD0, 0x42, 0xC7,
                    0x6E, 0x90, 0x00, 0xBE, 0x6F, 0x50, 0x01, 0xC5, 0xDA, 0x47, 0x3F, 0xCD, 0x69, 0xA2, 0xE2, 0x7A,
                    0xA7, 0xC6, 0x93, 0x0F, 0x0A, 0x06, 0xE6, 0x2B, 0x96, 0xA3, 0x1C, 0xAF, 0x6A, 0x12, 0x84, 0x39,
                    0xE7, 0xB0, 0x82, 0xF7, 0xFE, 0x9D, 0x87, 0x5C, 0x81, 0x35, 0xDE, 0xB4, 0xA5, 0xFC, 0x80, 0xEF,
                    0xCB, 0xBB, 0x6B, 0x76, 0xBA, 0x5A, 0x7D, 0x78, 0x0B, 0x95, 0xE3, 0xAD, 0x74, 0x98, 0x3B, 0x36,
                    0x64, 0x6D, 0xDC, 0xF0, 0x59, 0xA9, 0x4C, 0x17, 0x7F, 0x91, 0xBB, 0xC9, 0x57, 0x1B, 0xE0, 0x61,)
        self.PI = (self.pi0, self.pi1, self.pi2, self.pi3)
        assert self.n > 0

    @staticmethod
    def _size(hash_size: int):
        if 8 <= hash_size <= 256:
            return 512, 10, 8
        elif 256 < hash_size <= 512:
            return 1024, 14, 16
        raise ValueError("invalid hash size")

    @staticmethod
    def RLN(state: State, n) -> list:
        flattened_state = np.reshape(state, (1, len(state) * len(state[0])))
        first_n_elements = flattened_state[0][:n]
        return list(first_n_elements)

    def PSI(self, state: State) -> State:
        rows, cols = 8, self.c
        new_state = np.zeros((rows, cols), dtype=int)
        vector = np.array([0x01, 0x01, 0x05, 0x01, 0x08, 0x06, 0x07, 0x04], dtype=int)

        for i in range(rows):
            for j in range(cols):
                new_value = np.dot(state.state.T[j], np.roll(vector, i)) % 256
                new_state[i][j] = new_value

        return State(new_state)

    def zetaJV(self, j, v):
        result = [0xF3]
        for _ in range(6):
            result.append(0x00)
        xor_value = ((self.c - 1 - j) << 4) ^ v
        result.append(xor_value)
        return result

    def nuLV(self, v, X: State):
        new_X = State(np.copy(X))
        for column_id in range(len(new_X[0])):
            vector = self.zetaJV(column_id, v)
            new_X.addColumnMod(vector, column_id, 256)
        return new_X

    def piStroke(self, X: State):
        new_state = State(np.zeros((len(X), len(X[0])), dtype=int))
        for i in range(len(X)):
            for j in range(len(X[0])):
                new_state[i][j] = self.PI[i % 4][X[i][j]]
        return new_state

    def tauL(self, X: State):
        X = State(np.copy(X))
        for i in range(len(X)):
            if self.I == 512:
                if i <= 6:
                    X.shiftRows(i, i)
            elif self.I == 1024:
                if i <= 5:
                    X.shiftRows(i, i)
                else:
                    X.shiftRows(i, 10)
            else:
                raise ValueError("Invalid value of I")
        return X

    def TLXor(self, state: State):
        state = State(np.copy(state))
        for round_num in range(self.t):
            k_l_v_state = KLV(round_num, state)
            pi_stroke_state = self.piStroke(k_l_v_state)
            tau_l_pi_stroke_state = self.tauL(pi_stroke_state)
            state = self.PSI(tau_l_pi_stroke_state)
        return state

    def TLSum(self, X: State):
        X = State(np.copy(X))
        for v in range(self.t):
            X = self.PSI(self.tauL(self.piStroke(self.nuLV(v, X))))
        return X

    def hasher(self, h_k):
        T_l_xor = self.TLXor(h_k)
        final = np.bitwise_xor(T_l_xor, h_k)
        return bytes(self.RLN(final, self.n))

    def messageHashing(self, M: bytearray | bytes):
        M = self.messageDivider(self.bytesPadding(M))
        h_i = self.converterBytes(self.IV)
        for v in range(1, len(M) + 1):
            h_i_1 = self.TLXor(np.bitwise_xor(h_i, M[v - 1]))
            h_i_2 = self.TLSum(M[v - 1])
            h_i_3 = h_i
            h_i = State(np.bitwise_xor(np.bitwise_xor(h_i_1, h_i_2), h_i_3))
        return self.hasher(h_i)

    def bytesPadding(self, bytez: bytearray | bytes):
        block_size = self.I
        b = np.ceil(block_size / 8).astype(int)
        n1 = ((-self.N - 97) % self.I) // 8
        padding = bytearray([0x80] + [0x00] * n1)
        out = bytez + padding
        c = 12
        size = (b - ((len(out) + c) % b)) % b
        out += b"\x00" * size
        out += self.N.to_bytes(c, "little")

        return out

    def messageDivider(self, bytez: bytearray | bytes) -> list:
        block_size = self.I // 8
        num_blocks = len(bytez) // block_size
        states = []
        for i in range(num_blocks):
            state = self.converterBytes(bytez[i * block_size:(i + 1) * block_size])
            states.append(state)

        return states

    def converterBytes(self, vec: bytes) -> State:
        list_ = []
        for i in vec:
            list_.append(int(i))
        matrix = np.array(list_)
        reshaped_matrix = matrix.reshape((8, self.c))
        return State(reshaped_matrix)