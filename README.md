# LC_result_extracter

LC分析結果がまとまったtxtファイルから任意のデータを抽出するツールです。
一般的には以下のように実行します。

```
python LC_result_extracter.py [input_folder] -n [Compound_names] -t [Retention times]
```

あらかじめ `input_folder`にあたるフォルダーを作成し、その中にLC分析結果がまとまったtxtファイルを入れておいて下さい。

## テストケース
```
化合物名:x, Retention times:7.5
化合物名:y, Retention times:9.3
化合物名:z, Retention times:21.9
```
の場合以下のように実行します。

```
python LC_result_extracter.py output_190813 -n x,y,z -t 7.5,9.3,21.9
```

すると、 `output_190813`のフォルダー内に `output_190813.csv`というファイルが作成されています。
これを開くと、化合物x,y,zそれぞれのピーク面積が抽出されていることが分かります。

抽出するピークについては指定したRetention times±0.2 secのものを抽出します。
その付近に複数のピークがあると正しく抽出されない可能性があります。
