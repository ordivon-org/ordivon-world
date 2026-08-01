export class NonRetryableError extends Error {
  constructor(message, name = "NonRetryableError") {
    super(message);
    this.name = name;
  }
}
