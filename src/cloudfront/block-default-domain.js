function handler(event) {
    var request = event.request;
    var host = request.headers.host.value.toLowerCase(); // ホスト名を小文字に統一
    var uri = request.uri; // リクエストされたパスを取得

    console.log("Request Host:", host); // デバッグログ

    // CloudFrontのデフォルトドメインを含むアクセスを禁止
    if (host.includes('.cloudfront.net')) {
        console.log("Blocked request from:", host, "URI:", uri); // デバッグログ

        return {
            statusCode: 403,
            statusDescription: 'Forbidden',
            headers: {
                "content-type": { "value": "text/html" }
            },
            body: `<html><head><title>403 Forbidden</title></head><body><center><h1>403 Forbidden</h1></center></body></html>`
        };
    }

    // 許可されたドメインの場合はリクエストを続行
    return request;
}
