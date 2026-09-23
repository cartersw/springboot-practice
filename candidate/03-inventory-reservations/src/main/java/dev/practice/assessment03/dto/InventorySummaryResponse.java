package dev.practice.assessment03.dto;
public record InventorySummaryResponse(String sku,int availableQuantity,long reservedQuantity,long activeReservations) {}
