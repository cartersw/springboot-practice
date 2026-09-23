package dev.practice.assessment03.model;
import jakarta.persistence.*;import org.hibernate.annotations.Check;
@Entity @Table(name="reservation_lines",uniqueConstraints=@UniqueConstraint(columnNames={"reservation_id","sku"}))
@Check(constraints="quantity > 0") public class ReservationLine {
 @Id @GeneratedValue(strategy=GenerationType.SEQUENCE,generator="reservation_line_seq")
 @SequenceGenerator(name="reservation_line_seq",sequenceName="reservation_line_seq",allocationSize=1,initialValue=1000) private Long id;
 @ManyToOne(optional=false) @JoinColumn(name="reservation_id",nullable=false) private Reservation reservation;
 @ManyToOne(optional=false) @JoinColumn(name="sku",nullable=false) private StockItem stockItem;
 @Column(nullable=false) private Integer quantity;
 public ReservationLine(){}
 public Long getId(){return id;}public void setId(Long v){id=v;}
 public Reservation getReservation(){return reservation;}public void setReservation(Reservation v){reservation=v;}
 public StockItem getStockItem(){return stockItem;}public void setStockItem(StockItem v){stockItem=v;}
 public Integer getQuantity(){return quantity;}public void setQuantity(Integer v){quantity=v;}
}
