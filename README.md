# Contact Us Hub

## プロジェクト概要
このリポジトリは `contact-us-hub` に関する機能を提供します。

## ディレクトリ構成
```
├── .gitignore
├── README.md
├── buildspec.yml                    # ビルドスクリプト
├── src
│   ├── cfn
│   │   └── template.yaml            # Cfnテンプレート
│   ├── cloudfront
│   │   └── block-default-domain.js  # CloudFront 関数
│   └── lambda
│       └── contact_handler.py       # /contact へのPOSTメソッドに紐づくAPIソース
└── statics                          # 各種静的コンテンツ
    ├── index.html
    ├── main.css
    └── main.js
```


## 開発の進め方
- 開発にはGithub Flowを採用します
- `feature/*` ブランチで機能開発を行い、`main` ブランチにマージを行うことでリリースを行います
