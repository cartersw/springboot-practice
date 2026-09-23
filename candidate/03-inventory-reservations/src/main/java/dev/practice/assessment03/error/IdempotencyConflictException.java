package dev.practice.assessment03.error;
public class IdempotencyConflictException extends ApiException {public IdempotencyConflictException(){super(409,"IDEMPOTENCY_CONFLICT","Request key has different content");}}
