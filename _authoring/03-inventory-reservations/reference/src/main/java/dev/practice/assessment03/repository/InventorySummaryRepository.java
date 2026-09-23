package dev.practice.assessment03.repository;
import java.util.List;import org.springframework.stereotype.Repository;import org.springframework.jdbc.core.JdbcTemplate;import dev.practice.assessment03.dto.InventorySummaryResponse;
@Repository public class InventorySummaryRepository {
 private final JdbcTemplate jdbc;public InventorySummaryRepository(JdbcTemplate j){jdbc=j;}
 public List<InventorySummaryResponse> summary(){
  String sql="select s.sku,s.available_quantity,coalesce(sum(case when r.status='ACTIVE' then l.quantity else 0 end),0) reserved_quantity,count(distinct case when r.status='ACTIVE' then r.id end) active_reservations from stock_items s left join reservation_lines l on l.sku=s.sku left join reservations r on r.id=l.reservation_id group by s.sku,s.available_quantity order by s.sku";
  return jdbc.query(sql,(rs,i)->new InventorySummaryResponse(rs.getString("sku"),rs.getInt("available_quantity"),rs.getLong("reserved_quantity"),rs.getLong("active_reservations")));
 }
}
