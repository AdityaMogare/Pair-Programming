#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { flagSuspiciousEvents } = require("./detector");

const events = JSON.parse(
  fs.readFileSync(path.join(__dirname, "events.json"), "utf8")
);

const results = flagSuspiciousEvents(events);
const suspicious = results.filter((r) => r.suspicious);

console.log(
  `Scanned ${events.length} events — ${suspicious.length} suspicious\n`
);

suspicious
  .sort(
    (a, b) =>
      (b.severity ?? 0) - (a.severity ?? 0) || a.event_id.localeCompare(b.event_id)
  )
  .forEach((r) => {
    console.log(
      `  ${r.event_id}  severity=${r.severity ?? "?"}  [${r.reasons.join(", ")}]`
    );
  });
