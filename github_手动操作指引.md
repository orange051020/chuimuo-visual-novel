# GitHub 手动操作指引

当前状态：本地 Git 仓库已初始化，分支为 `main`。GitHub CLI 已安装，但当前未登录，因此不自动创建远端仓库、不写入账号凭证、不绕过认证。

## 步骤 1：登录 GitHub CLI

在项目根目录执行：

```powershell
gh auth login
```

按提示选择 GitHub.com、HTTPS、浏览器登录或设备码登录。登录完成后验证：

```powershell
gh auth status
```

## 步骤 2：创建公开仓库

登录成功后，在 `chuimuo-visual-novel/` 目录执行：

```powershell
gh repo create chuimuo-visual-novel --public --description "风暴中的大顺朝·垂暮序章 | 历史悬疑水墨风视觉小说" --source . --remote origin
```

如提示远端已存在，先检查：

```powershell
git remote -v
```

## 步骤 3：推送 main 分支

```powershell
git branch -M main
git push -u origin main
```

仓库地址格式应为：

```text
https://github.com/<你的用户名>/chuimuo-visual-novel
```

## 步骤 4：开启 GitHub Pages

进入 GitHub 仓库页面：

```text
Settings -> Pages
```

推荐配置：

- Source：GitHub Actions
- 使用仓库内 `.github/workflows/pages.yml` 自动部署 `build-web/`
- Enforce HTTPS：开启

如果改用分支部署：

- Source：Deploy from a branch
- Branch：`main`
- Folder：`/build-web`
- Enforce HTTPS：开启

## 当前阻塞说明

- 未登录 GitHub CLI 前，无法自动创建公开仓库。
- 美术素材未投放前，`build-web/` 只能保持工程准备状态，不能完成真实网页包验收。
