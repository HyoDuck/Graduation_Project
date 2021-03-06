msgs.df < - c()  # 빈 데이터프레임  생성
trending_stock < - c("SSNLF", "GILD")  # 주식종목 선택

stock_twits < - function(msgs.df, stock)
{
    # Get raw data
    url < - paste("https://api.stocktwits.com/api/2/streams/symbol/", stock, ".json", sep="")  # api로 부터 데이터 추출

msgs < - c()
for (i in c(1:length(url)))  # 전체 내용 행만큼 반복
{
raw < - readLines(url[i], warn="F")
resp < - fromJSON(raw)  # json 파싱
for (j in c(1:length(resp$messages)))
{
    msg < - unlist(resp$messages[j])
msgs < - rbind(msgs, c(msg["id"], msg["body"], msg["created_at"], stock[i]))  # id, 내용, 날짜, 주가종목 가져오기
}
}
eval.parent(substitute(msgs.df < - unique(rbind(msgs.df, msgs))))  # 행 덧붙이기
}

stock_twits(msgs.df, trending_stock)
write.csv(msgs.df, file="C:/Users/user1/stock-twits.csv",
          row.names = FALSE, col.names = FALSE, append = TRUE)  # 주가정보 저장될 경로 지정


