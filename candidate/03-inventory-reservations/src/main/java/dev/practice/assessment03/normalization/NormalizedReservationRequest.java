package dev.practice.assessment03.normalization;
import java.util.List;import dev.practice.assessment03.dto.ReservationItemResponse;
public record NormalizedReservationRequest(String requestKey,String customerRef,List<ReservationItemResponse> items,String canonicalPayload){public NormalizedReservationRequest{items=List.copyOf(items);}}
