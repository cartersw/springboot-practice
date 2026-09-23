package dev.practice.assessment02.model;
import jakarta.persistence.*;
@Entity @Table(name="products") public class Product {
 @Id private Long id;
 @Column(nullable=false,unique=true) private String sku;
 @Column(nullable=false,length=100) private String name;
 @Column(nullable=false,length=40) private String category;
 @Column(name="price_cents",nullable=false) private Integer priceCents;
 @Column(nullable=false) private Integer stock;
 public Product(){}
 public Long getId(){return id;}public void setId(Long v){id=v;}
 public String getSku(){return sku;}public void setSku(String v){sku=v;}
 public String getName(){return name;}public void setName(String v){name=v;}
 public String getCategory(){return category;}public void setCategory(String v){category=v;}
 public Integer getPriceCents(){return priceCents;}public void setPriceCents(Integer v){priceCents=v;}
 public Integer getStock(){return stock;}public void setStock(Integer v){stock=v;}
}
