## reChatGPT_auto

reChatGPT_auto 是由 [Pandora]([Pool Token (fakeopen.com)](https://ai.fakeopen.com/pool)) 提供支持的工具。

#### 下一阶段计划

1. 增加重试功能, 报错自动重试
2. 自动提取poolToken, 并支持一键更新fakeToken和poolToken, 同时保持值不变
3. 增加错误账号的excel表头

#### 功能:

该工具调用 Pandora 的 fakeopen 服务，将普通账号批量转换为 pooltoken，作为 API 调用的账号池。

#### 程序逻辑

1. 读取 Excel 文件的第一列作为账号，第二列作为密码。

2. 通过账号密码自动提取 access token。

3. 使用 access token 和 username 作为 fake token 的参数，提取 fake token。

4. 最后将信息存储到文件中。

5. 参数列表:

   `用户名	密码	 AccessToken  有效期   id_token   refresh_token	fake_token	unique_name`

#### 错误处理

- 当出现错误时，会将出现错误的账号保存在 Excel 文件中。
- 格式: `username`

#### 注意事项:

- 使用 username 作为 faketoken 的 unique_name，所以 fakeToken 并不会发生变化
- PoolToken 是从 Excel 文件中的第`7`个参数作为 fakeToken 提取的