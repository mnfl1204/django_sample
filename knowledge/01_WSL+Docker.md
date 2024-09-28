## WSL設定
①コントロール パネル\すべてのコントロール パネル項目\プログラムと機能   
② 「Windows の機能の有効化または無効化」をクリック  
③ 「Linux 用 Windows サブシステム」「仮想マシン プラットフォーム」にチェック
④ MicroSoftStoreからUbuntuなどの仮想マシンをインストール  
⑤ Ubuntu起動時にカーネル関連のエラーが発生したら、マイクロソフトの以下サイトから更新プログラムをダウンロード＆インストール  
```
https://learn.microsoft.com/ja-jp/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package
```
⑥ コマンドプロンプトで以下WSLのバージョン確認  
```
wsl -l -v

バージョンが2でなかった場合は以下を実行
wsl --set-version Ubuntu 2
wsl --set-default-version 2
```

## Docker設定
① 公式サイトからDocker for Windowsをダウンロード＆インストール 
```
https://docs.docker.com/desktop/install/windows-install/
```
② General > Use the WSL 2 based engine にチェック  
③ Resources > WSL integration > Ubuntu にチェック（Ubuntuの場合）  
④ Ubuntuのターミナルから以下のコマンドで疎通確認
```
docker ps
```