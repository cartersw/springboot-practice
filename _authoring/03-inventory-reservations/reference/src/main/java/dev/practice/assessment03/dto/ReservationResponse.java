package dev.practice.assessment03.dto;
import java.util.List;
public record ReservationResponse(long id,String requestKey,String customerRef,String status,List<ReservationItemResponse> items,int totalQuantity){public ReservationResponse{items=List.copyOf(items);}}
