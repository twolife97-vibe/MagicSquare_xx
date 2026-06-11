import { describe, expect, it } from "vitest";
import { add } from "./add";

describe("add", () => {
  it("정수 두 개를 더한다", () => {
    expect(add(2, 3)).toBe(5);
  });

  it("음수를 더한다", () => {
    expect(add(-2, 3)).toBe(1);
    expect(add(-2, -3)).toBe(-5);
  });

  it("실수를 더한다", () => {
    expect(add(1.5, 2.3)).toBeCloseTo(3.8);
    expect(add(-1.2, 0.5)).toBeCloseTo(-0.7);
  });

  it("0을 더해도 값이 유지된다", () => {
    expect(add(5, 0)).toBe(5);
    expect(add(0, -3.5)).toBe(-3.5);
  });

  it("NaN 입력 시 NaN을 반환한다", () => {
    expect(add(NaN, 1)).toBeNaN();
    expect(add(1, NaN)).toBeNaN();
  });

  it("Infinity 입력 시 JavaScript 덧셈 규칙을 따른다", () => {
    expect(add(Infinity, 1)).toBe(Infinity);
    expect(add(-Infinity, Infinity)).toBeNaN();
  });
});
