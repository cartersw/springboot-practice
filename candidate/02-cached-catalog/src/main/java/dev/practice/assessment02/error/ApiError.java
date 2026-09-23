package dev.practice.assessment02.error;
public record ApiError(int status, String code, String message, String path) {}
