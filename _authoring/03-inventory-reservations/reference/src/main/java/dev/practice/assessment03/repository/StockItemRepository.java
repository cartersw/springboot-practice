package dev.practice.assessment03.repository;
import dev.practice.assessment03.model.StockItem;import org.springframework.data.jpa.repository.JpaRepository;
public interface StockItemRepository extends JpaRepository<StockItem,String> {}
