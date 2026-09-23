package dev.practice.assessment01.error;
public record ApiError(int status, String code, String message, String path) {}
