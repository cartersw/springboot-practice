package dev.practice.assessment03.error;
public class StockNotFoundException extends ApiException {public StockNotFoundException(){super(404,"STOCK_NOT_FOUND","Stock item not found");}}
