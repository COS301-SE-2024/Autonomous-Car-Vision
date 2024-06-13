import { describe, expect, it, test } from 'vitest'

test("testing something", () => {
    expect(1 + 2).toBe(3)
})

describe("TESTING MULTIPLE", () => {
    it("1 + 1", () => {
        expect(1+1).toBe(2)
    })

    it("2 * 2", () => {
        expect(2 * 2).toBe(4)
    })
})

