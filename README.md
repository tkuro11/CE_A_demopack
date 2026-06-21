# CE_A_demopack

`pygame` + `numpy` で書かれた、レトロな **デモシーン (demoscene)** 風エフェクト集です。
「Computer Excise A (CompA-2026)」向けの教材・デモパックとして作成されています。

各スクリプトは単独で実行できる Python ファイルで、`numpy` のベクトル演算（ループを使わない配列処理）を使って、リアルタイムに映像エフェクトを生成しています。コードを読むことで、座標変換・極座標・スライス演算・カラーパレットなどの考え方を学べる構成になっています。

## デモ一覧

| ファイル | 内容 |
| --- | --- |
| `classic_fire.py` | クラシックな「ファイヤーエフェクト」。最下行に火種を置き、上方向へ拡散・冷却させるアルゴリズム。 |
| `fire_with_string.py` | 上記の炎エフェクトに、ランダムな単語が燃えながら浮かび上がる文字描画を追加したバージョン。 |
| `gravity_lense.py` | 2000個の粒子が中心の重力源に引かれて周回・崩壊していく N体っぽい重力シミュレーション。 |
| `moire.py` | 回転するグリッドと拡大縮小するグリッドを XOR 合成して作る、モアレ（干渉縞）アニメーション。 |
| `scroll_text.py` | サイン波で上下に揺れながら流れる、レトロな「スクロールテキスト」。 |
| `splash.py` | サイン波による座標ズラし（displacement map）で、水面のような歪みを表現するエフェクト。 |
| `tunnel.py` | 極座標変換を使った、奥に向かって進む「ワープトンネル」エフェクト。 |
| `tunnel2.py` | `tunnel.py` を発展させ、チェッカーボードのテクスチャマッピングとフォグ効果を加えたバージョン。 |

## 必要環境

- Python 3.12 以上
- 依存パッケージ（`pyproject.toml` に記載）
  - `numpy >= 2.4.6`
  - `pygame >= 2.6.1`

## セットアップ

[uv](https://docs.astral.sh/uv/) を使う場合:

```bash
git clone https://github.com/tkuro11/CE_A_demopack.git
cd CE_A_demopack
uv sync
```

`pip` を使う場合:

```bash
git clone https://github.com/tkuro11/CE_A_demopack.git
cd CE_A_demopack
pip install numpy pygame
```

## 実行方法

各スクリプトを個別に実行します。

```bash
uv run classic_fire.py
# もしくは
python classic_fire.py
```

ウィンドウ内で **Esc キー** または **ウィンドウを閉じる** ことで終了できます。

## ライセンス

MIT License
