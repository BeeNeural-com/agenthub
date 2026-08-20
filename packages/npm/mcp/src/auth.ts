/** Access-key gating — disabled until team rollout. Stubs kept for future use. */

export class AccessKeyError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "AccessKeyError";
  }
}

/** Access-key gate — disabled until team rollout. Always passes. */
export function verifyAccessKey(): void {
  // no-op
}
