package dev.practice.assessment03.service;
import java.util.*;import org.springframework.stereotype.Service;import org.springframework.transaction.annotation.Transactional;
import dev.practice.assessment03.model.*;import dev.practice.assessment03.dto.*;import dev.practice.assessment03.repository.*;import dev.practice.assessment03.normalization.*;import dev.practice.assessment03.audit.ReservationAudit;import dev.practice.assessment03.error.*;
@Service public class ReservationService {
 private final ReservationRepository reservations;private final ReservationLineRepository lines;private final StockItemRepository stock;private final ReservationRequestNormalizer normalizer;private final AvailabilityChecker availability;private final ReservationAudit audit;
 public ReservationService(ReservationRepository r,ReservationLineRepository l,StockItemRepository s,ReservationRequestNormalizer n,AvailabilityChecker a,ReservationAudit audit){reservations=r;lines=l;stock=s;normalizer=n;availability=a;this.audit=audit;}
 private long validId(long id){if(id<=0)throw new InvalidRequestException("ID must be positive");return id;}
 private Reservation find(long id){return reservations.findById(validId(id)).orElseThrow(ReservationNotFoundException::new);}
 private ReservationResponse response(Reservation r){var items=lines.findByReservationIdOrderByStockItemSkuAsc(r.getId()).stream().map(l->new ReservationItemResponse(l.getStockItem().getSku(),l.getQuantity())).toList();return new ReservationResponse(r.getId(),r.getRequestKey(),r.getCustomerRef(),r.getStatus().name(),items,items.stream().mapToInt(ReservationItemResponse::quantity).sum());}
 @Transactional
 public CreateReservationOutcome create(CreateReservationRequest input){
  var request=normalizer.normalize(input);var existing=reservations.findByRequestKey(request.requestKey());
  if(existing.isPresent()){var r=existing.get();if(!normalizer.samePayload(r.getCanonicalPayload(),request.canonicalPayload()))throw new IdempotencyConflictException();return new CreateReservationOutcome(response(r),false);}
  var r=new Reservation();r.setRequestKey(request.requestKey());r.setCustomerRef(request.customerRef());r.setStatus(ReservationStatus.ACTIVE);r.setCanonicalPayload(request.canonicalPayload());r=reservations.saveAndFlush(r);
  for(var item:request.items()){
   var s=stock.findById(item.sku()).orElseThrow(StockNotFoundException::new);availability.check(s.getAvailableQuantity(),item.quantity());
   s.setAvailableQuantity(s.getAvailableQuantity()-item.quantity());s=stock.saveAndFlush(s);
   var line=new ReservationLine();line.setReservation(r);line.setStockItem(s);line.setQuantity(item.quantity());lines.saveAndFlush(line);
  }
  audit.recordCreated(r.getId());return new CreateReservationOutcome(response(r),true);
 }
 @Transactional(readOnly=true) public ReservationResponse get(long id){return response(find(id));}
 @Transactional public ReservationResponse cancel(long id){
  var r=find(id);if(r.getStatus()==ReservationStatus.CANCELLED)return response(r);
  for(var line:lines.findByReservationIdOrderByStockItemSkuAsc(r.getId())){var s=stock.findById(line.getStockItem().getSku()).orElseThrow(StockNotFoundException::new);s.setAvailableQuantity(s.getAvailableQuantity()+line.getQuantity());stock.saveAndFlush(s);}
  r.setStatus(ReservationStatus.CANCELLED);r=reservations.saveAndFlush(r);audit.recordCancelled(r.getId());return response(r);
 }
}
