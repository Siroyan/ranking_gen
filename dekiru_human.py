# -*- coding: utf-8 -*-
# 画像の編集
from PIL import Image, ImageDraw, ImageFont
import discord
import asyncio
# 資格情報
import credentials
import re

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 文章から意識高いワードの含有率を返す
def detector(text):
    yokomoji_list = ['ディシジョン', 'ドラッカー', 'キックアウト', 'カタカナ・', 'ノー', 'プレスリリース', 'マーチレベル', 'テレカン', 'コスト', 'ニフティ', 'スキンシップ', 'マストアイテム', 'コイツ', 'ページ', 'スティーブジョブズ', 'ディスアグリー', 'アテンド', 'エンジン', 'インポータント', 'パワポ', 'スタイル', 'アセスメント', 'エラ', 'イジメ', 'ソーシャル・ディスタンシング', 'キャリア', 'タッチタイピング', 'デヴィ', 'スロット', 'パーセント', 'フォロワー', 'スピーカー', 'バカヤロー', 'プライバシーポリシー', 'ミックスジュース', 'ー', 'オーガニックユーザー', 'ポーズ', 'ハッタリバカ', 'スズメ', 'タワマン', 'ワクワク', 'イントネーション', 'イディオチック', 'オフショア', 'パートナー', 'プロ', 'メイキング', 'キャリッジ', 'オフショット', 'ドキュメント', 'フィジビリティスタディ', 'ヴィーガン', 'ドリフターズ', 'インフルエンサー・マーケティング', 'スタンプ', 'ソーシャル・ネットワーキング', 'ルール', 'クーラー', 'トレンド', 'コンビニ', 'ラーメン', 'コモディティ', 'ビューティクリニック', '・サジェスト', 'タップ', 'ジョーロ', 'コンセンサス', 'アボイド', 'オールモスト', 'ドタキャン', 'ファイナンシャル・プランナー', 'シュリンク', 'グレート', 'ペーシュ', 'リーズナブル', 'クルエルティフリー', 'コンテンツ', 'リスティング', 'ヶ', 'エサ', 'ノッピー', 'エンフルエンサー', 'プチプラパウダーファンデーション', 'ローマ', 'ヒガミ', 'ニーズ', 'ウジ', 'アフリカ', '・メーカー', 'メールマガジン', 'ツイッターユーザー', '・アパレル', 'シルバーライフ', 'シェアハウス', '・ゼネラリスト', 'イケイケ', 'サラダ', 'キャッチボール', 'キャッチフレーズ', 'ウロコ', 'パジェット', 'ネゴ', 'ドコモ', 'シカク', 'ポートフォリオ', 'プログラミング', 'オンスケ', 'トレンドスポット', 'ペン', 'レフ', 'ゴメーン', 'アレンジ', 'グランドデザイン', 'アメフト', 'アウトソージング', 'アナタ', 'デザイン・', 'シャッチョ', 'コンセプト', 'タレント', 'ドットシフォンスカート', 'ルーティン', 'ドーム', 'メディアユーザー', 'マルイ', 'シリーズ', 'インシデント', 'オワコン', 'グループディスカッション', 'ポンポン', 'デフレ', 'オール', 'ハリウッドスター', 'プロフィット', 'プレッシャー', 'アソブング', 'コミュ', 'ディズニーレポ', 'フリ', 'フラクトオリゴ', 'サーベイ', 'ビジネスパーソン', 'パラレル', 'コテハン', 'ワロタ', 'モンスターカスタマー', 'パーフェクト', 'オールウェイズ', 'エントリーシート', 'オーラ', 'エッセイ', 'カリスマ', 'ファン', 'パレート', 'シンキング', 'ネット', 'ラストオーダー', 'クリニック', 'リーマンショック', 'ヒント', 'アイテム', 'ケツ', 'ガンガンアウトプット', 'ウエディング', 'ポストコロナ', 'スリップ', 'ブロガー', 'トップス', 'ターゲット', 'ハングリー', 'オイルフリー', 'ビジネススキル', 'ドラマ', 'タルト', 'ゲイ', 'ストラテジ', 'ヴェリィ', 'ツイート', 'サブスクリプション', 'ウェブリオ', 'エクセレント・カンパニー', 'トルネ', 'ジャストアイデア', 'ワーク', 'アストラゼネカ', 'ギョウザ', 'キーワード', 'ウエスト', 'ジェネリック', 'スキル', 'ノマド', 'イニシアチブ', 'レッドオーシャン', 'ミニデスクトップ', 'ゴミ', 'スキーム', 'アンドゥ', 'ギレ', 'バミ', 'シェアオフィス', 'アルバイト', 'アーリーリタイアメント', 'ボランティア・', 'テラバイト', 'カーシェアリング', 'シャドーイング', 'カット', 'アイツ', 'ジョギング', 'グローバルリ', 'コンパクト', 'ナース', 'アブセンス', 'テレビ', 'コンサバ', 'ネクストクリエーション', 'ノリスケ', 'アグレッシブ', 'スイーツ', 'ネットワーキングパーティー', 'テクニカルターム', 'ビジョン', 'ウチ', 'ミエナイ', 'ハマ', 'ジャブラー', 'セキュリティ', 'ライフハック', 'タブレット', 'タダ', 'レポート', 'リアル', 'クマ', 'ペース', 'マキシマム', 'セットオン', 'バストアップ', 'クイズ', 'スラング', 'クリエイティブ', 'グロ', 'スレ', 'サイクル', 'スマホ', 'クチコミサイト', 'インターンシップ', 'メンタリティ', 'ポル', 'トライアル', 'ランチ', 'グリーングッズ', 'パターン', 'リスケジュール', 'プライド', 'ロックンロール', 'グリー', 'リモート', 'フォーカス', 'デュアルライフ', 'ビジネスサクセス', 'ヨハン・ヴォルフガング・フォン・ゲーテ', 'アプルーブ', 'トレース', 'トップ', 'ゴー', 'デカイ', 'インドネシア', 'アマゾン', 'ピカピカ', 'ゲット', 'キリ', 'バイリンガル', 'アイスブレイク', 'アイディア', 'ヨガ', 'サステナビリティ', 'オーガニックユーザ', 'ツインプラネット', 'メジャー', 'ポケモン', 'カフェ', 'メンバー', 'アベノーマル', 'スケージュール', 'バベル', 'ロングロング', 'エイサップ', 'ユーザー', 'ライフスタイル', 'クルーガー', 'ハタラクティブ', 'アヘッド', 'ジェット', 'フラペチーノ', 'ベトナム', 'アクセプト', 'ノイジーネイバー', 'スムージー', 'インフォームドコンセント', 'ウケ', 'クエスチョネア', 'ジャパン', 'ポータルサイト', 'リツイート', 'コール', 'キャスター・', 'レート', 'キツ', 'ハイコスト', 'ビッグ', 'ラッキーアイテム', 'カレンダー', 'カットマスク', 'ボ', 'チャリティー', 'ノヽ', 'ランキング', 'コンセント', 'ポスティング', 'サプリ', 'ソフト', 'アマゾンプライム', 'マラソン', 'イデオロギー', 'バスケット', 'コラボキャンペーン', 'タイト', 'クール', 'ブレーキ', 'イニシアティブ', 'オトモン', 'コミティア', 'オーストラリア', 'デート', 'スタンフォード', 'ロックダウン', 'マクドナルド', 'アイデンティティー', 'エンターテインメント', 'アウトバウンド', 'キャッチコピー', 'シニアマネージャー', 'ホテル', 'イメチェン', 'バリ', 'デンタルケア', 'ハレーション', 'コンシーラー', 'ストレッチ', 'タイムライン', 'チョコ', 'ストロー', 'クリスマス', 'ディーゼル', 'ファミマ', 'ニコル', 'オポチュニティマネージメント', 'キークエスチョン', 'コミュニケーションミス', 'グループ', 'マーケマーケ', 'アップ', 'ケチ', 'スポーツ', 'グサッ', 'スケベ', 'テクノロジー', 'イロイロ', 'コスプレ', 'フェルミ', 'ワザマエ', 'エネ', 'プライベートエピソード', 'ニューヨークタイムズベストセラー', 'アイス', 'タスマニア', 'スッキリ', 'コメント・シェア', 'ノンカフェイン', 'バタバタ', 'クビ', '・セリフ', 'スポット', 'コメントガイドライン', 'ボロボロ', 'ベネフィット', 'エンタメ', 'サビキ', 'コミット・コミットメント', 'ナウ', 'ターニングポイント', 'ブレイク', 'コマ', 'パフェ', 'データ', 'エスカレ', 'アイヌ', 'ハートウォーム', 'アクセント', 'ヒデヨシ', 'ガールズ', 'シースー', 'エスカレート', 'フロム', 'プロモーション', 'スタバマグ', 'スパッ', 'マックカフェ', '・バジェット', 'パーティー', 'ガールズウォーカー', 'コンテクスト', 'ジルスチュアート', 'ロシア', 'イジ', 'メイク', 'メールセミナー', 'ニコニコ', 'スクリーンショット', 'イワシ', 'フリーダム', 'スカスカ', 'フォトウエディング', 'ドン', 'チャンネー', 'ポジティブ', 'ゴーグル', 'トゥギャザー', 'ドラクエ', 'シャワーヘッド', 'センセーショナルファンタジー', 'ベラベラ', 'ダークドレアム', 'ブレインストーミング', 'レジデンス', 'ベストプラクィス', 'ヨダエ', 'ロケ', 'シングルタスク', 'ドック', 'アクティブ', 'エビダンス', '・コーディング', 'アクション', 'オーナー', '・サービス', 'オリ', 'スッピン', 'ジブリ', 'ラップトップ', 'ワーホリ', 'ママ', 'ポテト', 'レスポ', 'クソ', 'アンチエイジング', 'インド', 'ブック', 'ワー', 'エクスキュース', 'デファクトスタンダード', 'グッドポイント', 'ペンディング', 'ストレスフリー', 'ドリンク', 'マンネリ', 'スプーン', 'クライアントビジット', 'ファイナンス', 'リーダー', 'ファーストブリージング', 'レクチャー', 'イーエス', 'フォーマル', 'チャンス', 'アサップ', 'キャリアウーマン', 'ネガティブ', 'オネェ', 'スクショ', 'アダムス', 'コンサルフレームワーク', 'マーケ', 'ログイン', 'デファクト', 'ブックス', 'ミータス', 'マーケット', 'ワイフ', 'エール', 'コメ', 'アレコレ', 'バ', 'ヤンカー', 'ビジネスワード', 'コン', 'トリガートリガー', 'ページトップ', 'エンドユーザー', '・ハイキング', 'ドヤリング', 'キラーコンテンツ', 'ブルー', 'ライフ', 'ドキ', 'フレキシブル', '・ホラー', 'ブースト', 'クリスマスプレゼント', 'リオオリンピック', 'ニコ', 'リーマン・ショック', 'コアコンピタンス', 'ディサグリー', 'タカヤ', 'ナス', 'フットケア', 'ルーレット', 'プロフェッショナル', 'エリアターゲティング', 'スケール', 'デバフスキルナーフ', 'ニトリ', 'キズ', 'ボトルネック', 'カバー', 'テプラ', 'レポ', 'モロ', 'モチベーション', 'ム', 'ライフスタイルマガジン', 'ウズキャリ', 'セブン', 'プロセッコ', 'デビュー', 'ジーンズブランド', 'ド', 'オーバーコロナ', 'キャンキャン', 'エステ', 'モバイル', 'アピール', 'ブリーフィング', 'プライベートジム', 'ナチュラル', 'ヘルプ', 'ファッション', 'アグリー', 'ネットスラング', 'バイウィークリー', 'ユーザーベネフィット', 'キャリアデザイン', 'コンフリクト', 'マッチングサービス', 'ロサンゼルス', 'フレアパンツ', 'グチ', 'ワースト', 'ブイブイ', 'インセンティブ・モチベーション', 'タイアップ', 'マーチャンダイジング', 'ウィン・ウィン', 'イタリア', 'スパークリングワイン', 'クルーズシップ', 'ロジカルシンキング', 'ステーキ', 'ビル', 'ジェンダー', 'パパ', 'ピンク', 'フォロー', 'セミナー', 'メチャ', 'アウトサイドイン', 'ユニオンクエスト', 'アルコール', 'コスメ', 'シノアリス', 'スクール', 'クロスオフィス', 'ハシビロコ', 'シナジー', 'ウィンウィンウィンウィン', 'ノンネイティヴ', 'スタイリッシュ', 'ブラウザー', 'スケ', 'デメリット', 'ライフマガジン', 'コーデ', 'オッケー', 'バズプラス', 'ジム', 'マズロー', 'センス', 'プライオリティ', 'キャラペディア', 'フナカワ', 'セールス', 'ワンス・アポン・ア・タイム', 'マニフェスト', 'スマートインターチェンジ', 'イベント・', 'ヘッチャラ', 'ビンタ', 'アフィリエイト', 'メガネクイッ', 'ウチカレ', 'トレーニング', 'ストレス', '・イノベーション', 'カチャカチャ', 'レゴランド', 'リスニング', 'カンバセーション', 'ユーザ', 'サポーター', 'モン', '・サスナビリティ', 'クリック', 'キング', 'ブルーオーシャン', 'ベージュ', 'スピリチュアル', 'メルクマール', 'ゲッター', 'ガル', 'ドライバー', 'メリット・デメリット', 'アフター', 'コピーライター', 'グッド', 'ムダ', 'オフ', 'スタイリスト', 'コチラ', 'フリート', 'ドッグ', 'メンタリスト', 'メガテン', 'キャッシュフロー', 'エバンジェリスト', 'ヘーガイ', 'バター', 'クオリティ', 'ボリューム', 'ブーケ', 'キャッチアップ', 'ファクトベース', 'ペリー', 'アメージング', 'マンガ・', 'ワイン', 'サクサク', 'ギロッポン', 'カニバリ', 'ガリ', 'ムービー', 'メゾンメルカリ', 'オア', 'フリーランス', 'タンク', 'ジャンル', 'タッチ', 'ナビリティ', 'カードゲーム', 'ベース', 'ターン', 'メーカー', 'ン', 'ワンハンドグルメ', 'ポリ', 'ドットコム', 'ワカ', 'エクセレン', 'ソーファー', 'プレーヤー', 'ランクイン', 'サ', 'インテリ', 'ニキビ', 'オルタナティブ', 'アジェンデ', 'プライベート', 'サウスピーク', 'スムーズ', 'ミス', 'ロケットニュース', 'マーケティング', 'サードウェーブ', 'オチ', 'プライペート', 'ステークホルダー', 'ジャニー', 'リスク', 'ホワイト', 'イス', 'マイナス', 'フィーバー', 'センセーショナル', 'マネージメント', 'ディティール', 'ピュリファイ', 'シチュエーション', 'ピストン', 'イノベーティブ', 'アズスーンアズポッシブル', 'セックスレスカップル', 'レスト', 'キンタロー', 'オランダ', 'アホ', 'ミナミセミクジラ', 'インターネット', 'ディテール', 'アーリーアダプター', 'アサッフ', 'プロブレム', 'フレ', 'シーケンス', 'ボタン', 'エキサイトニュース', 'ダイアルアップ', 'オープン', 'ネーミング', 'グループワーク', 'ヨイショ', 'ホッ', 'オペレータ', 'バイト', 'アニメキャラクター', 'インプレッシブ', 'メンション', '・シソーラス・', 'テキトー', 'ダイブ', 'ベスト', 'カタカナルシスト', 'ゲーム', 'インテリア', 'ホルモンバランス', 'イマイチ', '・コンセンサス', 'オウム', 'ノートパソコン', 'ラウンジ', 'デイリー', 'ソサエティ', 'マルモ', 'ノウハウノート', 'チョコレートクインテット', 'ナチュラルインテリア', 'ジャイロ', 'ドンドン', 'ナニソレ', 'ガチャチケッ', 'クリエイター', 'パチンコ', 'パンツ', 'アカデミック', 'スライド', 'ムード', 'モンスターハンターストーリーズ', 'レンジ', 'オペレーション', 'ファイト', 'リ・スケジュール', 'メンタリズム', 'アイシー', 'エヴァンゲリオン', 'システムエンジニア', 'ムキ', 'オリンピック', 'サマライズ', 'サブミ', 'マーチ', 'ビハインド', 'チャラ', 'ハンバーガー', 'アプリケーション', 'マンキン', 'バラエティニュース', 'チカラ', 'ショートノーティス', 'プロジェクト', 'アウトレット', 'シンクロ', 'レイプ', 'ネットワーク', 'マシ', 'ガリガリペン', 'モデルプレス', 'ノルマ', 'フルコミット', 'デフォルト', 'アポ', 'ダイエット', 'ドミノピザ', 'キツイ', 'ニュース', 'フォロバ', 'ル', 'プレイリスト', 'ツアー', 'ラテン', 'リリース', 'コーパス', 'テスト', 'ドラスティック', 'アクセス', 'コレクター', 'ボーダーライン', 'サスペンス', 'ローンチ', 'インビテーション', 'アドレス', 'ストック', 'フォローワー', '・・', 'アトリビューションレポート', 'ツイッター', 'ジョブオープニング', 'プレジデントオンライン', '・クリエイター', 'ジャスト', 'アントレプレナーシップ', 'ハードル', 'ファーム', 'マイル', 'カテゴリ', 'ケア', 'バジェットプラン', 'カフェカフェ', 'ウマ', 'イメージダウン', 'クリ', 'テキストコミュニケーション', 'キー', 'ゴール', 'プライオリティー', 'ペルソナ', 'イタ', 'コミュニケーション', 'クラネオ', 'ロッド', 'ショートヘア', 'パイ', 'アーカイブ', 'スマートホーム', 'トピ', 'リザベーション', 'ーー', 'ハック', 'スプール', 'インフルエンザ', 'ミニ', 'オーライ', 'プロジェクションマッピング', 'パラ', 'ウイルスソフト', 'ナブル', 'アカデミー', 'セール', 'コレ', 'インスタグラマー', 'フェイスマ', 'ディスプレイ', 'アナフィラキシー', 'サジェスチョン', 'ボランティア', 'ジョブズ', 'ビジネスモデル', 'オーダーメイド', 'ニンジャ', 'バレ', 'トモノカイ', 'ベイタワー', 'ヘア', 'メイン', 'ミツマタウォッチ', 'メインメニュー', 'ミニマム', 'トラウマ', 'オポチュニティー', 'グーグル', 'エビフライ', 'サビキメバル', 'オールインワンジェル', 'コトワカ', 'コンピューター・ガジェット', 'ネック', 'カタルシス', 'ビジネスオンラインサロン', 'ターゲティング', 'インスタライブ', 'エネルギー', 'ベター', 'ドヤ', 'ステイ', 'ゼネラリスト', 'オシャレ', 'ムカ', 'デリバリ', 'アリ', 'デッドライン', 'サンフォロミー', 'セルフネイル', 'バリュー', 'ジェフウォーカー', 'ランダム', 'ルアー', 'サイン', 'アカウント', 'キャラ', 'ベッキ', 'ライフスタイルメディア', 'テーマパーク', 'リバイズ', 'ニキビ・シミ・クマ', 'ニュースメディア', 'ブランディング', 'グリーンティー', 'シリコンバレー', 'エクスキューズミー', 'ウィング', 'アイスブレーク', 'オレ', 'ファストフード', '・エビデンス', 'メソッド', 'カナダ', 'ライン', 'リソース', 'ト', 'キチン', 'ヨハネスブルク', 'プレイ', 'ジョイン', 'マターマター', 'フラ', 'ネットショッピング', 'バラ', 'エビエビ', 'マンション', 'ブサイク', 'ホント', 'パーツ', 'ニュースサイト', 'ブラック', 'ダニング', 'テンション', 'キーボード', 'ショート', 'プレゼンス', 'ファクト', 'アプリ', 'フレーバー', 'スキルアップ', 'ブラウザ', 'ケーズィー', 'タイム', 'インハウス', 'コンテンツ・マーケティング', 'イヤ', 'ニュークレアス', 'ワード', 'バジェット', 'ワンタスク', 'ポテンシャル', 'ガブリエル', 'クレジット', 'ブラインドタッチ', 'アイデア', 'ワナビー', 'バレンタインデー', 'カルタ', 'ワークポート', 'アクシスコンサルティング', 'テクニック・', 'オフィス', 'ビジネスプロセスアウトソーシング', 'デトックス', 'ホリデー', 'マカロン', 'ポイフル', 'フィリピン', 'ソリューション', 'タロット', 'タウンワークマガジン', 'ドンペリ', 'サカボン', 'ホスト', 'アジア', 'オポチュニティ', 'コミュニケーションコスト', 'メディアクレイジー', 'ポテチ', 'リーチ', 'ダイエットマイナス', 'オフセット', 'サプライズ', 'セブ', 'ダサ', 'ヤメヨウカナ', 'フィット', 'エピソード', 'パワースポット', 'スタンダード', 'スラスラ', 'シンギュラリティ', 'ベローチェ', 'エキスパート', 'グロースハック', 'サティスファクション', 'マーケティングイノベーション', 'アージェントマター', 'ファクター', 'エフワイアイ', 'コロナ', 'プラチナカード', 'サポートセンター', 'ユニット', 'ガジェット', 'サラリーマン', 'レッテル', 'モテ', 'ブロック', 'コイル', 'クリエーター', 'アイスブレイカー', 'サクッ', 'ググ', 'アサイニー', 'ジャストノーティス', 'ネタバレ', 'スルー', 'オピニオンリーダー', 'フォーム', 'ウエディングパーク', 'フレッシュ', 'タイトル・', 'ゥ', 'フッ', 'マイストアパスポート', 'ペットボトル', 'クラス', 'ススメ', 'ローンチパーティ', 'メリハリ', 'プログラミングサークル', 'シャンプーランキング', 'クリエイティブブリーフ', 'ヨハネスブルグ', 'オープニン', 'メモ', 'サーチナ', 'マイルストーン', 'グラップ', 'センテンス', 'エクセル', 'メルマガ', 'プラン', 'サイトマップ', 'マスタープラクショナー', 'ダイソー', 'シングルライフ', 'ペンギン', '・マーケティング', 'ロフト', 'イカ', 'サンクコスト', 'フレンド', 'コストパフォーマンス', 'ディスピュート', 'セラピスト', 'オーバー', 'オムニチャネル', 'シート', 'タンポン', 'キラキラネーム', 'ベストセラー', 'ギャグ', 'イノベーションイノベーション', 'フィジビリティ', 'ボクセルアート', 'ウスラカゲ', 'カジュアルコーデ', 'ジーンズ', 'オーバーシュート', '・デート・', 'ガバナンス', 'サマ', 'レ', 'オーガナイザー', 'リアルライブ', 'クレーム', 'ニニニニニニニニニ', 'ベッキー', 'ジャストアイディア', 'ワーケーション', 'セグメンテーション', 'ブリキ', 'モノ', '・エンタメ', 'フィックス', 'ジェーディー', 'チキンレース', 'フラッシュアイディア', 'ダメ', 'ナレッジ', 'ルー', 'メール', 'プラットフォーム', 'オンライン', 'ナウヤング', 'ストーリーテラー・', 'プレゼント', 'ルイヴィトン', 'シャドウイング', 'ウエパ', 'スイッチ', 'ループ', 'アンテナ', 'アグ', 'シャープ', 'パッ', '・セミナー', 'メニュー', 'ヘタ', 'ミュージックステーション', 'ウザ', 'ホワイトデー', 'アドバイザー', 'サルトル', 'サステ', 'レース', 'アナウンスメント', 'セルフ・ブランディング', 'オンラインコミュニティ', 'シッカリ', 'マイナビウーマン', 'ナショナル', 'プライベートモード', 'フォトグラファー', 'オファー', '・スラング', 'リモートワーク', 'ショップ', 'マル', 'ケド', 'ビジネスアドバイザー', 'クリア', 'ローソン', 'クリエイティビティ', 'ホリエモン', 'ロジック', 'クセ', 'マギー', 'ヘン', 'コメントデータ', 'エクスキューズ', 'セクハラ', 'アグリーメント', 'プチプラ', 'デザイン', 'ネットアンケート', 'ブログ', 'セリング', 'フェア', 'タガタメ', 'キメ', 'ネイティブ', '・カタカナ', 'ワンマン', 'ピン', 'インタビューサービス', 'スカート', 'ステープラー', 'ラッフル', 'コンテキスト', 'カテゴリー', 'モーニング', 'サードプレイス', 'メシ', 'ラジオライフ', 'ハムスター', 'ギズモード・ジャパン', 'チャレンジ', 'ガナドウ', 'ハッピー', 'ウェブ', 'モード', 'マネ', 'ワンピース', 'パプロフ', 'オピニオン', 'ラジオ', 'ショートストーリー', 'ナオン', 'カニバリゼーション', 'アベ', 'プチミーティング', 'ブランド', '・コミットメント', 'フランク', 'ショートムービー', 'ビジネス', 'レジュメ', 'イケメン', 'オトナ', 'メッセ', 'ハサミ', 'クチコミ', 'パフォーマンス', 'サリン', 'クラクラ', 'セット', 'エシカル', 'ストーリー', 'デビッド・ダニング', 'レイ', 'リストラ', 'モンキー', 'コツコツ', 'ボク', 'ミスリード', 'オブインポータンス', 'ピーチ・ボーイ', 'ファンタジー', 'アートホテル', 'グラビアアイドル', 'レポートメーカー', 'アイコン', 'ギフト', 'イメージ', 'ホームソリューション', 'サッカーサイト', 'プライムビデオ', 'ナイス', 'コミックマーケット', 'ポンプ', 'コンバージョンポイント', 'ホームページ', 'オミット', 'ビジネスメール', 'パワハラ', 'セーフサーチ', 'ヨムーノ', 'オルタナ', 'ドラッグストア', 'プロダクト', 'シャンプー', 'ジェンダーバイアス', 'リゾートウエディング', 'ニオイ', 'コーデアイデア', 'ディフィカルト', 'リマーケティング', 'スラムダンク', 'イミフ', 'リスケット', 'ヘビロテ', 'マンガ・ママナース', 'リーバイ・ストラウス', 'オタク', 'ライブ', 'マナー', 'パーソナルカラー', 'コンサルティングファーム', 'トップページ', 'ショット', 'ストーリーズ', 'オブザーバー', 'クリステル', 'アドバイス', 'マテリア', 'ダウンロード', 'インプリ', 'テーマ', 'タイピング', 'モンハンライズ', 'スケルトン', 'マーク', 'アカリマチ', 'ホスピタリティ', 'オンラインサロン', 'センシティブ', 'オファーボックス', 'キュート', 'パンプキン', 'カップル・', 'パイナップル', 'ガンガン', 'ビジネスシーン', 'ストイック', 'ック', 'キャンプ', 'アウトドア', 'クリティカル', 'コミュニティ', 'ライク', 'バナ', 'スケジュール', '・ー', 'オススメ', 'クロ', 'レシピ', 'プリペイドカード', 'ザギン', 'ワーママ', 'ディスカヴァー・トゥエンティワン', 'キャンディデイト', 'フォーミュラ', 'ポンチ', 'イベント', 'ロングノーティス', 'マス', 'グルーピング', 'メッセージ', 'オオカミ', 'トータル', 'ウラカシ', 'チームリーダー', 'モンハンストーリーズ', 'カンファレンス', 'マウント', 'ステークスホルダー', 'フォトサイト', 'ソルトルアー', 'ヤバ', 'ヨルグラ', 'テンプレート', 'デパート', 'マネジメント', 'ベースメイクアップコレクション', 'アジェンダアジェンダ', 'プロフェッショナリズム', 'ドラッグストア・デパコス', 'リクワイアメント', 'ビール', 'ディフォールトゥ', 'フィーディング', 'アジェンダ', 'アポイントメント', 'ブログランキング', 'アスリート', 'シェフ', '・コンピテンシー', 'ランチメニュー', 'モラル', 'ブラッシュアップ', 'メンタル', 'バスト', 'エコ', 'ガチガチ', 'スマート', 'シャワー', 'マグネットク', 'フラワーアレンジメント', 'トップクラス', 'ハッキリ', 'インタイム', 'ナチュラルウェディング', 'ニューノーマル', 'ウォニョン', 'グロテスク', 'ハーブ', 'コバヤシモンド', 'フラッペ', 'スープ', 'プロジェクトメンバー', 'スクリーニング', 'ブレーンストーミング', 'ニューストップ', 'パン', 'ドアチャイム', 'マウンティング', 'ヒューマンスキル', 'コワーキングスペース', 'トラブル', '・パチ', 'ゲン', 'メールアドレス', 'フォローアップ', 'ギフトカード', 'ゴリ', 'ラクレ', 'イグジット', 'フリーザ', 'インフォーム', 'ボーナスゼロ', 'ハンドルネーム', 'デバイスメーカー', '・データ', 'サイネージ', '・アジェンダ', 'ベネフィーク', 'アチコチ', 'ビジネスマン', 'ケツカッチン', 'コントロール', 'ツインテール', 'イヤミ', 'アイドルグループ', 'アウトプット', 'オンサイト', 'クリーム', 'エニタイム', 'オピニョン', 'リズム', 'リスクヘッジメソッド', 'ザーボン', 'ディスア', 'ジレンマ', 'スパ', 'レベル', 'スターズ', 'スタンプ・', 'イブニング', 'インフルエンサーマーケティング', 'コンサルタント', 'マテリアルサイエンス', 'プレゼン', 'バケーション', 'エアコン', 'クライテリオン', 'ファッション・', 'ミーティング', 'アプロプリエット', 'キャンペーン', 'カルテ', 'コバヤシ', 'インスタグラム', 'デシジョン', 'デパコスパウダーファンデーション', '・・・', 'ゴールド', 'マイノリティ', 'イントロ', 'コラム', 'コンサル', 'テクニック', 'グランドオープン', 'サート', 'マネタイズ', 'リンク', 'マンガ', 'スクロール', 'ピル', 'ビジネススキーム', 'ヌード', 'エフアイワイ', 'パラダイムシフト', 'カースト', 'シンポジウム', 'イトイ', 'パードゥン', 'メイクセンス', 'サステナブル', 'フランス', 'キャズム', 'アジャイル', 'ターイム', 'イタイ', 'サッ', 'ボールペン', 'ネゴシエーション', 'スカ', '・ビジネス', 'メンター', 'ファシリテーター', 'ハーブティー', 'サポート', 'ワザワザ', 'クリティカルヒット', 'ノマドワーカー', 'ア', 'セブンカフェ', 'バランス', 'インスタ', 'ディス', 'ポリバレントプレーヤー', 'ダイバーシティ', 'ピッタマスク', 'クライアント', 'ボトル', 'ギャップ', 'タイミング・', 'サブスク', 'カウントダウンタイマー', 'ハロー', 'モヤ', 'クラブ', 'クランケ', 'オンラインビジネス', 'ヤツ', 'アウトソーシング', 'コーチングスクール', 'リフレッシュ', 'コンサルティング', 'オッサン', 'トゲ', 'ノシ', 'インターナル', 'アミノバザラシ', 'ノ', 'カメラ', 'アンケート', 'アジア・バロメーター', 'ジャンプ', 'ネットブログ', 'ザワ', 'サイゼリヤ', 'イノベーション', '・エリア', 'メバル', 'スクリーン', 'ゲスト', 'カフェイン', 'メダリスト', 'プレゼント・キャンペーン', 'インディーズマンガ', 'ギリギリ', 'ソーシャルイノベーションマガジン', 'ドライブ', 'シフト', 'ビスケット', 'スカートパンツ', '・ヴェブレン', 'ウォルトディズニー', 'ノロウィルス', 'コトバ', 'マター', 'シンエヴァ', 'イオナズン', 'レトロ', 'トマトパスタ', 'ハーゲンダッツ', 'コンバージョン', 'ニュージーランド', 'ドキドキ', 'コピペ', 'アカンパニー', 'スタバ', 'ワイファイ', '・イタ', 'アンデッド', 'イモ', 'ギャル', 'ユーザーガイド', 'アウト', 'マニア', 'ポンコツ', 'ニアミス', 'イン', 'リファレンスチェック', 'リスケ', 'クイック', 'アフィリエイター', 'コンプラ', 'マイルド', 'バイナリ', 'コラムニスト', 'マシン', 'オンスケジュール', 'ゲンダイ', '・リスケ', 'プロアクティブ', 'ホンモノ', 'ノーサイド', 'ワケ', 'レジ', 'プッシュ', 'ニュアンス', 'チア', 'ウクライナ', 'カッコ', 'トレ', 'イラッ', 'アイビー・リーグ', 'キュン', 'ドイツ', 'ブレスト', 'アライアンス', 'キュレーション', 'エスターク', 'ハローワーク', 'ロックマン', 'サイマルテニアスリィ', 'プロデューサー', 'マイページ', 'パーカッション・', 'カンパニー', 'デンマーク', 'コツ', 'ハイテンション', 'アレ', 'ストーリークエスト', 'リクルート', 'スピーチ', 'リンクママ', 'フリーター', 'セメント', 'ラジオドラマ', 'シェアボタン', 'イラストレーター', 'ブラックアルバイト', 'スティール・ボール・ラン', 'ウォッチ', 'シティボーイ', 'エクアドルケツヲ', 'パワーワード', 'ブックマークボタン', 'キロ', 'マッチポンプ', 'アナリティクス', 'グルメ', 'サーバ', 'サイト', 'フカン', 'キビ', 'アンガーマネジメント', 'オトク', 'ピアノ・', 'ウェイ', 'ホッチキス', 'エンジニアリング', 'カッコイイ', 'フリー', 'フィジビリ', 'ガイドライン', 'インプリフェーズ', 'エステサロン', 'トルコ', 'イ', 'ガムシャラ', 'カモフラージュ', 'キブナ', 'トランスナショナル', 'ステータスレポート', 'ウィキペディア', 'メープル', 'マスカルポーネ', '・クイズ', 'キャップ', 'スニーカー', 'ワープア', 'ショッピング', 'サムソン', 'バカ', 'ソフトロー', 'タイムテーブル', 'フォトジェニック', 'テトリス', 'ハドル', 'ハラスメント', 'プライム', 'グロス', 'ピコ', 'ブログランキング・', 'ワンウェイ', 'ブルベ', 'サイドビジネス', 'カノ', 'サイダー', 'チ', 'ヒアリング', 'クラスター', 'イライラ', 'ステップ', 'メレンゲ', 'エリートビジネスマン', 'ニート', 'イシュー', 'カルテットコミュニケーションズ', 'フリーランスエンジニア', 'モヤモヤ', 'トライ', 'メリット', 'ジュワ', 'パンツコーデ', 'シニアライフ', 'アディショナル', 'フットセラピー', 'アライン', 'プレジデント', 'マッチ', 'パスケース', 'スタンス', 'アップボート', 'サイズ', 'パソコン', 'オーガニック', 'アイドル', 'アマゴ', 'ツール', 'スキルセット', 'アプリダウンロード', 'カスタマー', 'インプット', 'リアルビジネス', 'ビッチ', 'ピーク', 'メルカリ', 'ノウハウ', 'ベンダー', 'スーツ', 'イラスト', 'エリート', 'アプライ', 'ブタ', 'サムネイル', 'テキストチャット', 'バレン', 'デパコス', 'ファインダー', 'ベンチャー', 'ヨダエリ', 'イライラサ', 'ト・', 'イエロー', 'ホットヨガ', 'デキル', 'オブジェクト', 'ログハウス', 'スタッフ', 'ヘルシー', 'チーズ', 'フレームワーク', 'ビックリ', 'セルフブランディング', 'ノート', 'ネタキャラ', 'メダル', 'コンシェルジュ', 'プライオリティナンバー', 'オフィシャルブログ', 'リサーチ', 'フツー', 'マリンスポーツ', 'サバ', 'セクシー', 'エイプリルフール', 'コピー', 'ガチナチュラル', 'コンゴ', 'ナルシスト', 'ラグビー', 'エントリー', 'タメ', 'オポテュニティ', 'テント', 'ニンニクヌキヤサイマシマシ', 'イレブン', 'ドキッ', 'スコア', 'インターン', 'クリスマススワッグ', 'ウーバーイーツ', 'アシスタント', 'コーヒー', 'マイナビエージェント', 'マイルドライナー', 'マネー', 'ライト', 'ジャニオタ', 'バリバリ', 'キッチン', 'インプレッション', 'サマリー', 'ヤマレコ', 'ボード', 'スマートフォン', 'ポイント', 'ファースト', 'オリジナル', 'ライバル', 'ステキ', 'マイルドカフェオーレ', 'スケープコート', 'メン', 'ビブラテルム', 'チェック', 'インルエンサー', 'スプレッドシート', 'グラスロッド', 'トリガー', 'プロモーションコード', 'ボルダリング', 'インタビュー', 'ガッチリ', 'イヤイヤ', 'モチベ', 'スーパー', 'ハングアウト', 'プレビュー', 'インタラクティブ', 'トン', 'シャド', 'キャスター', 'ヘアカラー', 'チャット', 'ティラミス', 'ゲー', 'ヘッジ', 'ダリア', '・プラント', 'レッツゴーカク', 'ウラニズム', 'トーク', 'サイクリング', 'エッチ', 'カタカナ', 'マグロ', 'トゥーゴー', 'エビデンス', 'タイプ', 'アタシ', 'ミュージック', 'インプルーブ', 'インバウンド', 'ベンチャー・', 'コスパ', 'アチュラチュ', 'リア', 'ブー', 'ブレイクダウン', 'ログインページ', 'ライセンス', 'アニワン', 'ガッキー', 'インターン・', 'アップデート', 'マタ', 'アバンギャルド', 'ベストプラクティス', 'コミットメント', 'ロングセラー', 'メンテナンス', 'コントローラー', 'マーケティング・プロモーション', 'マジ', 'ワット', 'ナイトブラ', 'インセンティブ', 'ユーチューバー', 'グランブルーファンタジー', 'フェアトレード', 'ビジネスマナー', 'プロダクトローンチフォーミュラー', 'イキイキ', 'タフ', 'フォームオーバーサブスタンス', 'ブドウ', 'タイミング', 'カンタン', 'フラット', 'ポジティブ・シンキング', 'マジョリティ', 'カスタムメイド', 'シナジィ', 'ソーシャル', 'ジョッキー', 'マニュアル', 'グラスファイバー', '・メリット', 'イージィ', 'プランニング', 'マスター', 'ウエディングドレス', 'シンク', 'ユーザーフレンドリー', 'ダイアリー', 'ズレ', 'モンスタ', 'マジイラ', 'ゼロベース', 'アドマーケティング', 'メカニズム', 'ブリリアント', 'フォーユアインフォメーション', 'ディープフェイク', 'デキ', 'ザ・ポジティブ', 'クーポン', 'プラス', 'テレワークライフ', 'ドラックスト', 'ブランドクリエイティブ', 'ベネフィット・リード・セラピー', 'デパートメント', 'スポンサーリンク', 'ドライフラワー', 'バブル', 'セルフプランニング', 'ラブラブ', 'リサイクル', 'プレミアム', 'スピード', 'アフターコロナ', 'マネージャークラス', 'バックグラウンドビデオ', 'ロードマップ', 'サービス', 'カップル', 'シベリアンハスキー', 'ウィル・スミス', 'エッ', 'ワクチン', 'ウィンウィン', 'ジョブ', 'パワフル', 'カ', 'ダンス', 'ベネ', 'リスト', 'ミシガン', 'フレーズ', 'フルメイク', 'コンサート', 'オーソライズ', 'キャリアアップ', 'コレクション', 'ビ', 'タイトル', 'ナチュラルサロンアベイユ', 'インスタンス', 'ワザ', 'ジャニーズ', 'トラフ', 'オウチーノ', 'マインド', 'ノンジャンル・メディア', 'オーケー', 'ノリ', 'イラ', 'ガールズチャンネル', 'ノーモララー', 'ウ', 'フェーズ', 'アコム', 'ポエム', 'フロー', 'バトル', 'コンプライアンス', 'トラベル', 'ネタ', 'マツエク', 'アメリカ', 'ライザップ', 'アクティブリスニング', 'プリン', 'コーディネート', 'マーケター', 'グランデフェス', 'ワッツ', 'スコーピオン', 'スゴイ', 'セルフスターター', 'シャンパンタワー', 'レビュー', 'メリバ', 'ピザハット', 'アン', 'フィードバックフィードバック', 'コミック', 'ソースコード', 'チャンネル', 'バイアニュアル', 'ビジュ', 'スポニチアネックス', 'ボス', 'レベルアップ', 'アセット', 'アクセスマップ', 'ニュージョイナー', 'ディレクター', 'フィージブル', 'ネイル', 'ネイティブキャンプ', 'ヤセ', 'スパム', 'モデリング', 'バイアス', 'ロゴ', 'カリフォルニア', 'アクセストレイラー', 'モノマネ', '・インタビュー', 'バラエティ', 'モロニック', 'レストラン', 'エスカレーション', 'ライター・', 'エンジニア', 'クリーニング', 'ウォーク', 'ガクチカ', 'アピール・', 'ロジカル', 'リラックスウェア', 'タイ', 'アビューシブ', 'ブックマーク', 'デー', 'ケース', 'オールカラー', 'ベクトル', 'トリビア', 'ソフトウェア', 'シェア', 'フィードバック', 'コンプレックス', 'マッチング', 'コメント', 'エージェント', 'ショートパンツ', 'イケ', 'フィールド', 'カレント', 'セリア', 'イチロー', 'ミサワ', 'ノーリターン', 'スタート', 'カルト', 'ビーセレクト', 'エリア', 'マスク', 'ピンポイント', 'ウエディングパークグループ', 'プロミス', 'バッファ', 'アドプション', 'スキー', 'プロセス', 'ブレーキペダル', 'タスク', 'テレワーク', 'アベイラブル', 'コンプリート', 'ライター', '・ノウハウ', 'タピオカ', 'ブレイン', '・アニメ', 'トイレ', 'リバウンド', 'イエベ', 'アントレプレナー', 'デコレ', 'プロボノ', 'アッポーペン', 'ピッタリ', 'ホバート', 'トク', 'アクティビティ', 'クーポンコード・キャンペーン', 'フォース', 'オンライントレーニング', 'ラベル', 'メディア', 'プチ', 'フェイスマスク', 'クレヨンタイプ', 'アニュアル', 'キレ', 'サッパリ', 'レッド', 'エモーショナル', 'ミツマタ', 'デジョン', 'バカリズム', 'ボディスーツ', 'コンサルタント・プリセールス', 'イコール', 'ファジィ', 'ピックアップ', 'オプション', 'クーポンコード', 'スターグループ', 'マン', 'マネージャー', 'サラッ', 'スカートコーディネート', 'アプローチ', 'マスト', 'サウンドシアターユニット', 'アカウントフォロー', 'オーケーベイベー', 'インパクト', 'リマインド', 'システム', 'オン', 'エグゼクティブ', 'ジョブプライオリティ', 'パトロール', 'ストレート', 'リラックス', 'パーティ', 'シーン', 'フェミニン', 'ラシッサ', 'ブーム', 'アサイン', 'ベンチマーク', 'グローバル', 'ダイビング', 'サークル', 'ブ', 'コンチプラン', 'カウント', 'ガイド', 'スゴ', 'スターバックス', 'リクルートグループサイト', 'グレードアップ', 'トリアエズデンシャヤバスガキケン', 'ボタニカル', 'シビア', 'リテラシー', 'カタカナビジネス', '・アグリー', 'オーシャン', 'コンピテンシー', 'チーム', 'ステータス', 'ストップ', 'ショック', 'グランピング', 'ツッコ', 'クライテリア', 'ビジネスセミナー', 'オトナンサー', 'カゴパク', 'フロア', 'ミッション', 'バナナ', 'デザインアズアンエンジニアリング', 'エクスプレッション', 'コラボ', 'アニメ', 'シンプル', 'コース', 'リチウム', 'モチーフ', 'フェース', 'レス', 'キャノン', '・', 'アグアグアグ', 'アラサー', 'スコティッシュフォールド', 'バイタリティ', 'ボイス・オブ・ユース', 'プロフィール', 'ウンコー', 'リアサイン', 'バンドマン', 'パラレルワールド', 'ヵ', 'マルチタスク', 'スケジューリング', 'シーズン', 'コンピュータ', 'クリスマスリース', 'モデル', 'エヴァ', 'アカ', 'スポ', 'カタカタ', 'コミット', 'エビ', 'ファイル', 'コンポーザー', 'プチプラ・デパコス・', 'ソーシャルディスタンス', '・メール', 'キャパオーバー', 'コード', 'プリクラ', 'アンバランス', 'ボケ', 'モラハラ', 'デイリーユース', 'スタグラム', 'ダブリューエフエイチ', 'スペック', 'インフレ', 'キープ', 'ニュープロダクト', 'マンパワー', 'サッカー', 'ファイナンシャルプランナー', 'ヒューマントラスト', 'トピック', 'リュック', 'スタートライン', 'フェイスブック', 'キジ', 'ボディ', 'アハモ', 'マスターベーション', 'オリックス', 'オンショアメンバー', 'ヤング', 'リップ', 'インフルエンザー', 'スケープゴート', 'ツラ', 'シ', 'フレックス', 'ペースダウン', 'コロナウイルス', 'インフルエンサー', 'クレイジー', 'ストリート', 'ビジネスチャンス', 'アー']

    p = re.compile('[\u30A1-\u30FF]+')
    text_list = p.findall(text)
    match_list = list(set(text_list) & set(yokomoji_list))
    if len(text_list) != 0:
        score = len(match_list) / len(text_list) * 100
    else:
        score = 0

    return str(round(score, 1)) + '%'

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

@client.event
async def on_message(message):
    if message.content=="$deki-hu":
        await message.channel.send('テキストを入力...')
        wait_message = await client.wait_for('message')
        sentence = wait_message.content
        result = detector(sentence)

        # background color : cream
        im = Image.new("RGB", (1200, 800), (255, 255, 254))
        draw = ImageDraw.Draw(im)
        # title
        font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-ExtraBold.ttf", size=100)
        draw.text((60, 60), 'できるHUMAN度は...', fill=(9, 64, 103), font=font)

        font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=200)
        w = font.getsize(result)[0]
        h = font.getsize(result)[1]
        draw.text(((1200 - w) / 2, (800 - h) / 2), result, fill=(9, 64, 103), font=font)

        image_filepath = './assets/images/dekiru_human_score.jpg'
        im.save(image_filepath, quality=100)
        await message.channel.send(file=discord.File(image_filepath))

# Botの起動とDiscordサーバーへの接続
client.run(credentials.DISCORD_TOKEN)

