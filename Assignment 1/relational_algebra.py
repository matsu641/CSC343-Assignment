"""
関係代数操作の実装
Relational Algebra Operations Implementation
"""

from typing import Set, Tuple, Dict, Any, Callable, List
from dataclasses import dataclass
import copy


# 関係（Relation）をタプルの集合として表現
Relation = Set[Tuple[Any, ...]]


class RelationalAlgebra:
    """関係代数の操作を提供するクラス"""
    
    @staticmethod
    def select(relation: Relation, condition: Callable[[Tuple], bool], 
               attr_names: List[str] = None) -> Relation:
        """
        選択操作 (σ - Selection)
        条件を満たすタプルのみを返す
        """
        return {t for t in relation if condition(t)}
    
    @staticmethod
    def project(relation: Relation, indices: List[int]) -> Relation:
        """
        射影操作 (Π - Projection)
        指定された列のみを抽出
        """
        return {tuple(t[i] for i in indices) for t in relation}
    
    @staticmethod
    def rename(relation: Relation) -> Relation:
        """
        リネーム操作 (ρ - Rename)
        属性名を変更（Pythonではタプルなので実際の実装は省略）
        """
        return copy.deepcopy(relation)
    
    @staticmethod
    def union(relation1: Relation, relation2: Relation) -> Relation:
        """
        和集合 (∪ - Union)
        """
        return relation1 | relation2
    
    @staticmethod
    def intersection(relation1: Relation, relation2: Relation) -> Relation:
        """
        積集合 (∩ - Intersection)
        """
        return relation1 & relation2
    
    @staticmethod
    def difference(relation1: Relation, relation2: Relation) -> Relation:
        """
        差集合 (- Difference)
        """
        return relation1 - relation2
    
    @staticmethod
    def cartesian_product(relation1: Relation, relation2: Relation) -> Relation:
        """
        直積 (× - Cartesian Product)
        """
        return {t1 + t2 for t1 in relation1 for t2 in relation2}
    
    @staticmethod
    def natural_join(relation1: Relation, relation2: Relation, 
                    r1_indices: List[int], r2_indices: List[int]) -> Relation:
        """
        自然結合 (⋈ - Natural Join)
        指定された列が等しいタプルを結合
        """
        result = set()
        for t1 in relation1:
            for t2 in relation2:
                # 結合条件をチェック
                if all(t1[i1] == t2[i2] for i1, i2 in zip(r1_indices, r2_indices)):
                    # 重複列を除いて結合
                    new_tuple = t1 + tuple(t2[i] for i in range(len(t2)) 
                                          if i not in r2_indices)
                    result.add(new_tuple)
        return result
    
    @staticmethod
    def theta_join(relation1: Relation, relation2: Relation, 
                   condition: Callable[[Tuple, Tuple], bool]) -> Relation:
        """
        θ結合 (⋈θ - Theta Join)
        条件を満たすタプルのペアを結合
        """
        result = set()
        for t1 in relation1:
            for t2 in relation2:
                if condition(t1, t2):
                    result.add(t1 + t2)
        return result


def print_relation(name: str, relation: Relation, attr_names: List[str] = None):
    """リレーションを見やすく表示"""
    print(f"\n{name}:")
    if not relation:
        print("  (empty)")
        return
    
    if attr_names:
        print(f"  {attr_names}")
    
    for i, t in enumerate(sorted(relation), 1):
        print(f"  {i}. {t}")
    print(f"  Total: {len(relation)} tuples")


if __name__ == "__main__":
    # 簡単なテスト
    ra = RelationalAlgebra()
    
    # テストリレーション
    R = {(1, 'Alice'), (2, 'Bob'), (3, 'Charlie')}
    S = {(1, 100), (2, 200), (4, 400)}
    
    print("Test Relations:")
    print_relation("R", R, ['id', 'name'])
    print_relation("S", S, ['id', 'score'])
    
    # 射影
    projected = ra.project(R, [0])
    print_relation("π[0](R)", projected, ['id'])
    
    # 選択
    selected = ra.select(S, lambda t: t[1] >= 150)
    print_relation("σ[score>=150](S)", selected, ['id', 'score'])
    
    # 直積
    product = ra.cartesian_product(R, S)
    print_relation("R × S", product, ['id1', 'name', 'id2', 'score'])
    
    # 自然結合
    joined = ra.natural_join(R, S, [0], [0])
    print_relation("R ⋈ S", joined, ['id', 'name', 'score'])
