/**
 * Pair programming starter — implement flagSuspiciousEvents().
 *
 * Each event:
 * {
 *   id: "evt_001",
 *   timestamp: "2025-07-09T14:30:00Z",
 *   actor: { user_id: "alice", ip: "..." },
 *   action: "token.access",
 *   resource: { type: "canary_token", id: "tok_prod_api" },
 *   geo: { country: "US", region: "..." }  // may be null
 * }
 *
 * Return one result per input event:
 * { event_id, suspicious, reasons, severity }
 */

/**
 * @param {object[]} events
 * @returns {object[]}
 */
function flagSuspiciousEvents(events) {
  return events.map((event) => ({
    event_id: event.id,
    suspicious: false,
    reasons: [],
    severity: 0,
  }));
}

module.exports = { flagSuspiciousEvents };
