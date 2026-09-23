package dev.practice.assessment03.error;
public class InsufficientStockException extends ApiException {public InsufficientStockException(){super(409,"INSUFFICIENT_STOCK","Insufficient available stock");}}
