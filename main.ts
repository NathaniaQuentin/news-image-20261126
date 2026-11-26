// "The World in One Day" — news-image-20261126 (Node 22, standard library only).
// The entry image news.png (1024x1024, drawn at build time by render.py) sits
// beside this file. This program writes it to /output/entry.png, validating it
// first so a corrupt or wrong-sized file can never reach the judge, and then
// proving the landed copy is byte-identical to the validated source.
// No network, no child processes, no writes outside the output directory.
// The output directory itself is never deleted: it is only created if missing,
// and entry.png is written alongside anything already there.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1048576;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
// A whole PNG ends with the 12-byte IEND chunk: length 0, "IEND", CRC ae426082.
const IEND_TAIL = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);

const sourcePath = new URL("./news.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destPath = join(outDir, "entry.png");

// Read the source exactly once: the bytes validated below are the bytes written.
const data = readFileSync(sourcePath);

if (data.length > MAX_BYTES) {
  throw new Error(`news.png is ${data.length} bytes, over the 1 MiB limit`);
}
if (data.length < 45 || !data.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("news.png does not start with the PNG magic bytes");
}
if (data.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("news.png has no IHDR chunk where one is expected");
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  throw new Error(`news.png is ${width}x${height}, expected 1024x1024`);
}
if (!data.subarray(data.length - 12).equals(IEND_TAIL)) {
  throw new Error("news.png is truncated: it does not end with an IEND chunk");
}
const sourceHash = createHash("sha256").update(data).digest("hex");

mkdirSync(outDir, { recursive: true });
writeFileSync(destPath, data);

const landed = readFileSync(destPath);
const landedHash = createHash("sha256").update(landed).digest("hex");
if (landedHash !== sourceHash) {
  throw new Error(
    `entry.png landed with sha256 ${landedHash}, expected ${sourceHash}`,
  );
}
const landedSize = statSync(destPath).size;
console.log(
  `wrote ${destPath} (${landedSize} bytes, 1024x1024 PNG, sha256 ${landedHash})`,
);

