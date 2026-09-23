package dev.practice.assessment03.dto;
public record CreateReservationRequest(String requestKey,String customerRef,java.util.List<ReservationItemRequest> items) {}
