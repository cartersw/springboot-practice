package dev.practice.assessment03.model;
import jakarta.persistence.*;
import org.hibernate.annotations.Check;
@Entity @Table(name="stock_items") @Check(constraints="available_quantity >= 0") public class StockItem {
 @Id @Column(length=32) private String sku;
 @Column(name="display_name",nullable=false) private String displayName;
 @Column(name="available_quantity",nullable=false) private Integer availableQuantity;
 public StockItem(){}
 public String getSku(){return sku;}public void setSku(String v){sku=v;}
 public String getDisplayName(){return displayName;}public void setDisplayName(String v){displayName=v;}
 public Integer getAvailableQuantity(){return availableQuantity;}public void setAvailableQuantity(Integer v){availableQuantity=v;}
}
