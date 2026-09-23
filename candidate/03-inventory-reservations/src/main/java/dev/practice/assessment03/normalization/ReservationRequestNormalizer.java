package dev.practice.assessment03.normalization;
import java.util.*;import com.fasterxml.jackson.databind.ObjectMapper;import org.springframework.stereotype.Component;
import dev.practice.assessment03.dto.*;import dev.practice.assessment03.error.InvalidRequestException;
@Component public class ReservationRequestNormalizer {
 private final ObjectMapper mapper;public ReservationRequestNormalizer(ObjectMapper m){mapper=m;}
 private String required(String s,int max){if(s==null||s.strip().isEmpty()||s.strip().length()>max)throw new InvalidRequestException("Missing or invalid text");return s.strip();}
 public NormalizedReservationRequest normalize(CreateReservationRequest r){
  String key=required(r.requestKey(),64),customer=required(r.customerRef(),64);
  if(!key.matches("[A-Za-z0-9_-]+"))throw new InvalidRequestException("Invalid request key");
  if(r.items()==null||r.items().isEmpty()||r.items().size()>20)throw new InvalidRequestException("Items must contain 1 to 20 entries");
  Map<String,Integer> merged=new TreeMap<>();
  for(var item:r.items()){
   if(item==null)throw new InvalidRequestException("Item required");
   String sku=required(item.sku(),32);
   if(!sku.matches("[A-Za-z0-9-]+"))throw new InvalidRequestException("Invalid SKU");
   if(item.quantity()==null||item.quantity()<1||item.quantity()>100)throw new InvalidRequestException("Invalid quantity");
   merged.put(sku,item.quantity());
  }
  var items=merged.entrySet().stream().map(e->new ReservationItemResponse(e.getKey(),e.getValue())).toList();
  try{String canonical=mapper.writeValueAsString(List.of(customer,items.stream().map(i->List.of(i.sku(),i.quantity())).toList()));return new NormalizedReservationRequest(key,customer,items,canonical);}catch(Exception e){throw new IllegalStateException("Cannot encode request",e);}
 }
 public boolean samePayload(String saved,String incoming){try{return mapper.readTree(saved).get(1).equals(mapper.readTree(incoming).get(1));}catch(Exception e){throw new IllegalStateException(e);}}
}
