# CSC343 Assignment 3 - README

## 1. 目的
このフォルダは CSC343 Assignment 3 の提出物をまとめたものです。
Part 1（設計・データ・SQLクエリ）と Part 2（FD/正規化の記述）を含みます。

## 2. 提出ファイル
Part 1:
- `schema.ddl`: スキーマ定義（制約、仮定、未実装制約の説明コメント付き）
- `data.sql`: テストデータ投入
- `q1.sql` - `q4.sql`: 問題1〜4のクエリ
- `runner.txt`: まとめ実行用スクリプト
- `demo.txt`: 実行ログ（クエリ本文と出力結果を両方含む）

Part 2:
- `a3.pdf`: 提出用PDF
- `a3.txt`: Part 2 の本文（PDF生成元）
- `a3.tex`: 参照用TeX版（提出の必須ではない）

## 3. 実行方法（Part 1再現手順）
このディレクトリで以下を実行:

```bash
/opt/homebrew/opt/postgresql@16/bin/psql -a -d postgres -f runner.txt > demo.txt
```

- `-a` を付けることで、`demo.txt` に「実行したSQL文」と「結果」の両方が出力されます。
- `runner.txt` は `schema.ddl` -> `data.sql` -> `q1.sql` -> `q4.sql` の順で実行します。

## 4. 設計メモ（schema.ddlに記載済み）
### 4.1 assertions/triggers なしでは厳密に表現できない制約
- `Ticket.seat_id` が `Ticket.concert_id` の venue と一致すること
- `ConcertSectionPrice.section_id` が `ConcertSectionPrice.concert_id` の venue と一致すること

### 4.2 追加で入れた制約
- `Venue(city, street_address)` を `UNIQUE`
- `Ticket(concert_id, seat_id)` を `UNIQUE`（同一席の二重販売防止）
- `ConcertSectionPrice(concert_id, section_id)` を `UNIQUE`

## 5. 目視テスト結果サマリ（PASS/FAIL）
判定根拠は `demo.txt` の最終出力。

| 項目 | 要件 | 結果(目視) | 判定 |
|---|---|---|---|
| Q1 | 3件以上のconcert、1件は50枚以上、1件は0枚、1件は0〜50枚 | 55枚 / 0枚 / 8枚 を確認（合計4行） | PASS |
| Q2 | 5行以上、かつ1 owner が3会場以上所有 | 6行、`Aurora Entertainment Group = 3` | PASS |
| Q3 | 10会場以上、各会場10席以上、少なくとも1会場が25%以上accessible | 10行、全会場10席以上、50%/60%会場あり | PASS |
| Q4 | 最多購入枚数が25以上（同率なら全員表示） | `powerbuyer = 35` | PASS |

## 6. 目視確認しやすい抜粋（demo.txtより）
### Q1（販売数条件）
- `City Lights Festival -> tickets_sold = 55`
- `Acoustic Night -> tickets_sold = 0`
- `Retro Rewind -> tickets_sold = 8`

### Q2（owner件数条件）
- `Aurora Entertainment Group -> venue_count = 3`
- 出力行数 `(6 rows)`

### Q3（venue/seat/accessibility条件）
- 出力行数 `(10 rows)`
- `Harbour Dome -> seat_count = 60, pct_accessible = 50.00`
- `Midtown Pavilion -> seat_count = 10, pct_accessible = 60.00`

### Q4（最多購入条件）
- `powerbuyer -> ticket_count = 35`

## 7. 最終チェックリスト
提出前に以下を確認:
- [x] `demo.txt` に SQL 文と結果が両方ある
- [x] `schema.ddl`, `data.sql`, `q1.sql` - `q4.sql` が存在
- [x] `a3.pdf` が存在
- [x] PASS/FAIL 判定を README で明示
