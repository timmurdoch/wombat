import { describe, expect, it } from "vitest";

import { getSuggestedCRS } from "../crs-suggestions";

const codes = (wkt: string) => getSuggestedCRS(wkt).map((s) => s.code);

describe("getSuggestedCRS, Australia", () => {
  it("suggests GDA2020, GDA94 and the matching MGA zone for Sydney", () => {
    const sydney = "POLYGON((151.1 -33.95, 151.3 -33.95, 151.3 -33.8, 151.1 -33.8, 151.1 -33.95))";
    const result = codes(sydney);
    expect(result).toEqual(expect.arrayContaining(["7844", "4283", "7856"]));
    expect(result).not.toContain("7855");
    expect(result).not.toContain("7850");
  });

  it("suggests only zone 55 for Melbourne to Canberra (west of 150°E)", () => {
    const result = codes("POLYGON((144.9 -37.9, 149.2 -37.9, 149.2 -35.2, 144.9 -35.2, 144.9 -37.9))");
    expect(result).toContain("7855");
    expect(result).not.toContain("7856");
  });

  it("suggests both zones for data crossing the 150°E boundary", () => {
    const result = codes("POLYGON((148 -36, 152 -36, 152 -33, 148 -33, 148 -36))");
    expect(result).toEqual(expect.arrayContaining(["7855", "7856"]));
  });

  it("suggests no Australian CRS for European data", () => {
    const berlin = "POLYGON((13.3 52.4, 13.5 52.4, 13.5 52.6, 13.3 52.6, 13.3 52.4))";
    expect(codes(berlin).some((c) => c.startsWith("78") || c === "4283")).toBe(false);
  });
});
