package dev.practice.assessment03.error;
public record ApiError(int status, String code, String message, String path) {}
