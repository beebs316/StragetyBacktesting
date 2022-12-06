from polygon import RESTClient
import numpy as np
import talib as ta
import json
import requests
import pprint
import datetime
from datetime import timedelta
import pandas as pd

key = ""
client = RESTClient(key)




def my_function(joe, ticker, timeframe, ema_1_temp, ema_2_temp):

    # Define today.
    startdate1 = datetime.datetime.now() - timedelta(days=joe)
    today_00 = datetime.datetime.now() - timedelta(days=joe)
    weekday = today_00.weekday()



    if weekday == 0:
        startdate1 = datetime.datetime.now() - timedelta(days=joe+3)


    startdate = startdate1.strftime("%Y-%m-%d")
    enddate = today_00.strftime("%Y-%m-%d")



    holiday = 0
    # holidays
    if today_00.month == 4 and today_00.day == 2:
        holiday = 1
    if today_00.month == 2 and today_00.day == 17:
        holiday = 1
    if today_00.month == 1 and today_00.day == 20:
        holiday = 1
    if today_00.month == 1 and today_00.day == 1:
        holiday = 1
    if today_00.month == 12 and today_00.day == 25:
        holiday = 1
    if today_00.month == 11 and today_00.day == 26:
        holiday = 1
    if today_00.month == 9 and today_00.day == 2:
        holiday = 1
    if today_00.month == 6 and today_00.day == 4:
        holiday = 1
    if today_00.month == 5 and today_00.day == 27:
        holiday = 1
    if today_00.month == 7 and today_00.day == 5:
        holiday = 1
    if today_00.month == 5 and today_00.day == 31:
        holiday = 1
    if today_00.month == 9 and today_00.day == 6:
        holiday = 1

    if weekday < 5 and holiday == 0:


        data1m = client.stocks_equities_aggregates(ticker, timeframe, "minute", startdate, enddate)
        if data1m.results == None:
            return None

        data1m = list(data1m.results)
        an_array1m = np.array(data1m)

        i1m = 0
        closeData = []
        closeData1 = []
        timeData = []
        vwapData = []
        highData = []
        openData = []
        lowData = []
        lowData1 = []
        highData1 = []
        timeData1 = []
        slowkData = []
        cross_2 = 0
        count = 0
        startcount = 0
        last_slowk = 0
        last_upperband = 0
        last_lowerband = 0
        last_close = 0
        delta_slowk = 0
        break_stochrsi = 0
        break_bband = 0
        ellie = 0
        i = 1
        e = 0

        test_high = 0
        test_low = 0
        test_high1 = 0
        test_low1 = 0

        data_1 = 0
        data_2 = 0
        data_3 = 0
        timedata_1 = 0
        timedata_2 = 0
        timedata_3 = 0
        closedata_1 = 0
        closedata_2 = 0
        closedata_3 = 0
        mom_cross_up = 0
        mom_cross_down = 0
        mac_cross_up = 0
        mac_cross_down = 0
        stoch_green = 0
        stoch_red = 0
        macd_green = 0
        macd_red = 0
        en = 0
        en2 = 0
        en_up = 0
        en_up2 = 0
        en_down = 0
        en_down2 = 0
        startcount1 = 0
        startcount2 = 0
        delta = 0
        time_data2 = 0



        while i1m == 0:
            joe = an_array1m[count]
            values_array = np.array(list(joe.values())).flatten()

            volume = values_array[0]
            vwap = values_array[1]
            open = values_array[2]
            close = values_array[3]
            high = values_array[4]
            low = values_array[5]
            time = values_array[6]
            date1 = datetime.datetime.fromtimestamp(time / 1000.0)

            if date1.hour >= 7:
                timeData.append(date1)
                closeData.append(close)
                highData.append(high)
                lowData.append(low)
                openData.append(open)
                vwapData.append(vwap)
                jose = pd.DataFrame(closeData, columns=['Close_one_min'])
                jose1 = pd.DataFrame(highData, columns=['High'])
                jose2 = pd.DataFrame(closeData, columns=['Low'])

                # BBAND DATA
                jose['upper_band'], jose['middle_band'], jose['lower_band'] = ta.BBANDS(jose['Close_one_min'],
                                                                                        timeperiod=20)

                jose['slowk'], jose['slowd'] = ta.STOCH(jose1['High'], jose2['Low'], jose['Close_one_min'], fastk_period=3, slowk_period=10, slowk_matype=0, slowd_period=10,
                                     slowd_matype=0)

                jose['mom'] = ta.MOM(jose['Close_one_min'], timeperiod=12)

                jose['macd'], jose['macdsignal'], jose['macdhist'] = ta.MACDFIX(jose['Close_one_min'], signalperiod=10)

                jose['ema_1'] = ta.EMA(jose['Close_one_min'], timeperiod=ema_1_temp)
                jose['ema_2'] = ta.EMA(jose['Close_one_min'], timeperiod=ema_2_temp)

                jose['ma_200'] = ta.EMA(jose['Close_one_min'], timeperiod=20)
                jose['rsi_1'] = ta.RSI(jose['Close_one_min'], timeperiod=14)

                rsi_1 = jose['rsi_1']
                ma_200 = jose['ma_200']
                ema_1 = jose['ema_1']
                ema_2 = jose['ema_2']
                upper_band = jose['upper_band']
                middle_band = jose['middle_band']
                lower_band = jose['lower_band']
                macd = jose['macd']
                macdsignal = jose['macdsignal']
                macdhist = jose['macdhist']
                slowk = jose['slowk']  # green
                slowd = jose['slowd']  # red

                mom = jose['mom']
                if date1.hour <= 9:
                    if date1.hour == 9 and date1.minute > 30:
                        early = 0
                    else:
                        early = 1


                else:
                    early = 0
                if date1.hour == 10 and date1.minute >= 50:
                    early = 1




                if date1.day == today_00.day and early == 0 and date1.hour <= 10:
                    last_mom = mom[startcount - 1]
                    close = closeData[startcount]
                    vwap_close = vwapData[startcount]
                    rsi_1_1 = rsi_1[startcount-1]
                    last_mom_2 = mom[startcount - 2]
                    mom = mom[startcount]
                    last_macd = macd[startcount-1]
                    last_macdsignal = macdsignal[startcount-1]
                    last_ema_1 = ema_1[startcount - 1]
                    ema_1_1 = ema_1[startcount]
                    last_ema_2 = ema_2[startcount - 1]
                    ema_2_1 = ema_2[startcount]
                    ma_200_1 = ma_200[startcount]
                    last_slowk = slowk[startcount-1]
                    last_slowk_1 = slowk[startcount-2]
                    slowk_1 = slowk[startcount]

                    if slowk[startcount] > (slowd[startcount]):
                        stoch_green = 1
                    else:
                        stoch_green = 0
                    if slowk[startcount] < (slowd[startcount]):
                        stoch_red = 1
                    else:
                        stoch_red = 0
                    if macd[startcount] > macdsignal[startcount]:
                        macd_green = 1
                    else:
                        macd_green = 0
                    if macd[startcount] < macdsignal[startcount]:
                        macd_red = 1
                    else:
                        macd_red = 0





                    if macd[startcount-1] < macdsignal[startcount-1] and macd[startcount] > macdsignal[startcount] and en == 0 and close > vwap_close:
                        startcount1 = startcount
                        mac_cross_up = 1
                        en = 1
                        en_up = 1





                if date1.day == today_00.day and date1.hour >= 15:
                    time_data = timeData[startcount1]
                    time_data2 = timeData[startcount2]
                    if en_up2 == 0 and en_down2 == 0:
                        open_data2 = 0
                    else:
                        open_data2 = openData[startcount2 + 1]

                    open_data = openData[startcount1 + 1]

                    if en == 0:
                        list_1 = 0, 0, open_data, open_data2, mac_cross_up, mac_cross_down, test_high, test_low, test_high1, test_low1
                        return list_1


                    if en == 1:
                        test_high = highData[startcount1 + 1]
                        if highData[startcount1+2] > test_high:
                            test_high = highData[startcount1 + 2]
                        if highData[startcount1 + 3] > test_high:
                            test_high = highData[startcount1 + 3]
                        if highData[startcount1 + 4] > test_high:
                            test_high = highData[startcount1 + 4]
                        if highData[startcount1 + 5] > test_high:
                            test_high = highData[startcount1 + 5]
                        if highData[startcount1 + 6] > test_high:
                            test_high = highData[startcount1 + 6]
                        if highData[startcount1 + 7] > test_high:
                            test_high = highData[startcount1 + 7]
                        if highData[startcount1 + 8] > test_high:
                            test_high = highData[startcount1 + 8]
                        if highData[startcount1 + 9] > test_high:
                            test_high = highData[startcount1 + 9]
                        if highData[startcount1 + 10] > test_high:
                            test_high = highData[startcount1 + 10]
                        if highData[startcount1 + 11] > test_high:
                            test_high = highData[startcount1 + 11]
                        if highData[startcount1 + 12] > test_high:
                            test_high = highData[startcount1 + 12]
                        if highData[startcount1 + 13] > test_high:
                            test_high = highData[startcount1 + 13]


                        test_low = lowData[startcount1 + 1]
                        if lowData[startcount1 + 2] < test_low:
                            test_low = lowData[startcount1 + 2]
                        if lowData[startcount1 + 3] < test_low:
                            test_low = lowData[startcount1 + 3]
                        if lowData[startcount1 + 4] < test_low:
                            test_low = lowData[startcount1 + 4]
                        if lowData[startcount1 + 5] < test_low:
                            test_low = lowData[startcount1 + 5]
                        if lowData[startcount1 + 6] < test_low:
                            test_low = lowData[startcount1 + 6]
                        if lowData[startcount1 + 7] < test_low:
                            test_low = lowData[startcount1 + 7]
                        if lowData[startcount1 + 8] < test_low:
                            test_low = lowData[startcount1 + 8]
                        if lowData[startcount1 + 9] < test_low:
                            test_low = lowData[startcount1 + 9]
                        if lowData[startcount1 + 10] < test_low:
                            test_low = lowData[startcount1 + 10]
                        if lowData[startcount1 + 11] < test_low:
                            test_low = lowData[startcount1 + 11]
                        if lowData[startcount1 + 12] < test_low:
                            test_low = lowData[startcount1 + 12]

                        if en2 == 1:
                            test_high1 = highData[startcount2 + 1]
                            if highData[startcount2 + 2] > test_high1:
                                test_high1 = highData[startcount2 + 2]
                            if highData[startcount2 + 3] > test_high1:
                                test_high1 = highData[startcount2 + 3]
                            if highData[startcount2 + 4] > test_high1:
                                test_high1 = highData[startcount2 + 4]
                            if highData[startcount2 + 5] > test_high1:
                                test_high1 = highData[startcount2 + 5]
                            if highData[startcount2 + 6] > test_high1:
                                test_high1 = highData[startcount2 + 6]
                            if highData[startcount2 + 7] > test_high1:
                                test_high1 = highData[startcount2 + 7]
                            if highData[startcount2 + 8] > test_high1:
                                test_high1 = highData[startcount2 + 8]
                            if highData[startcount2 + 9] > test_high1:
                                test_high1 = highData[startcount2 + 9]
                            if highData[startcount2 + 10] > test_high1:
                                test_high1 = highData[startcount2 + 10]

                            test_low1 = lowData[startcount2 + 1]
                            if lowData[startcount2 + 2] < test_low1:
                                test_low1 = lowData[startcount2 + 2]
                            if lowData[startcount2 + 3] < test_low1:
                                test_low1 = lowData[startcount2 + 3]
                            if lowData[startcount2 + 4] < test_low1:
                                test_low1 = lowData[startcount2 + 4]
                            if lowData[startcount2 + 5] < test_low1:
                                test_low1 = lowData[startcount2 + 5]
                            if lowData[startcount2 + 6] < test_low1:
                                test_low1 = lowData[startcount2 + 6]
                            if lowData[startcount2 + 7] < test_low1:
                                test_low1 = lowData[startcount2 + 7]
                            if lowData[startcount2 + 8] < test_low1:
                                test_low1 = lowData[startcount2 + 8]
                            if lowData[startcount2 + 9] < test_low1:
                                test_low1 = lowData[startcount2 + 9]
                            if lowData[startcount2 + 10] < test_low1:
                                test_low1 = lowData[startcount2 + 10]
                        else:
                            time_data2 = 0


                        list_1 = time_data, time_data2, open_data, open_data2, mac_cross_up, mac_cross_down, test_high, test_low, test_high1, test_low1
                        return list_1

                    en = 0
                    en2 = 0
                    mac_cross_up = 0
                    mac_cross_down = 0
                    startcount1 = 0
                    startcount2 = 0

                    list_1 = time_data, time_data2, open_data, open_data2, mac_cross_up, mac_cross_down, test_high, test_low, test_high1, test_low1
                    return list_1





                    #print('Time :', timeData[startcount])
                    #print('Close :', closeData[startcount])
                    #print('MOM :', mom[startcount])
                    #print(slowk[startcount])
                    #print(slowd[startcount])
                    #print('')
                    # print(last_slowk)
                    # print('')








                # break down

                # if last_slowk != slowk[startcount]:
                # last_slowk = slowk[startcount]

                startcount = startcount + 1

            count = count + 1

            if count == 400:
                startcount = 0
                count = 0
                i1m = 1


def runbacktest(ticker, timeframe):
    ema_1_temp = 2
    ema_2_temp = ema_1_temp
    x = 0
    test_count = 0
    rate1 = 0
    rate2 = 20
    ema1best = 0
    ema2best = 0

    while x < 14:
        jo = 1
        right = 1
        wrong = 0
        confirmed1 = 0
        confirmed2 = 0
        target = 0
        target_delta = 0
        pt_target = 0
        day = 0
        avg = 0
        miss = 0
        miss1 = 0
        pt = 0
        pt2 = 0

        import datetime

        while jo <= 80:

            list_1 = my_function(jo, ticker, timeframe, ema_1_temp, ema_2_temp)
            jo = jo + 1
            if list_1 == None:
                wrong = 1
            else:
                day = day + 1
                time_data, time_data2, close_data, close_data1, cross_up, cross_down, test_high, test_low, test_high1, test_low1 = list_1
                pt_target = close_data * .006
                # print(day)


                if cross_up == 1:
                    confirmed1 = confirmed1 + 1
                    delta = test_high - close_data
                    if delta >= pt_target:
                        pt = pt + 1
                    else:
                        miss = miss + 1
                    accuracy = pt / confirmed1

                    if day == 30:
                        if confirmed1 >= rate1 or confirmed1 >= 20:
                            if miss < rate2 and ema_1_temp != ema_2_temp:
                                rate1 = confirmed1
                                rate2 = miss
                                ema1best = ema_1_temp
                                ema2best = ema_2_temp
                        print('Test:', test_count + 1, ' EMA:', ema_1_temp, ema_2_temp, ' Rate: ', confirmed1, miss)
                        # print('EMA_2 = 2 ,', ema_2_temp)
                        # print('Rate: ', confirmed1, miss)
                        # print('Days confirmed: ', confirmed1)
                        # print('Days confirmed but missed PT: ', miss)
                        # print('________________________________________________')
                        # print('')

                if cross_down == 1:
                    confirmed1 = confirmed1 + 1
                    delta = close_data - test_low
                    if delta >= pt_target:
                        pt = pt + 1
                    else:
                        miss = miss + 1
                    accuracy = pt / confirmed1

                    if day == 30:
                        if confirmed1 >= rate1 or confirmed1 >= 20:
                            if miss < rate2 and ema_1_temp != ema_2_temp:
                                rate1 = confirmed1
                                rate2 = miss
                                ema1best = ema_1_temp
                                ema2best = ema_2_temp

                        print('Test:', test_count + 1, ' EMA:', ema_1_temp, ema_2_temp, ' Rate: ', confirmed1, miss)
                        # print('EMA_2 = 2 ,', ema_2_temp)
                        # print('Rate: ', confirmed1, miss)
                        # print('Days confirmed: ', confirmed1)
                        # print('Days confirmed but missed PT: ', miss)
                        # print('________________________________________________')
                        # print('')

                if cross_up == 0 and cross_down == 0:
                    if day == 30:
                        if confirmed1 >= rate1 or confirmed1 >= 20:
                            if miss < rate2 and ema_1_temp != ema_2_temp:
                                rate1 = confirmed1
                                rate2 = miss
                                ema1best = ema_1_temp
                                ema2best = ema_2_temp
                        print('Test:', test_count + 1, ' EMA:', ema_1_temp, ema_2_temp, ' Rate: ', confirmed1, miss)
                        # print('EMA_2 = 2 ,', ema_2_temp)
                        # print('Rate: ', confirmed1, miss)
                        # print('Days confirmed: ', confirmed1)
                        # print('Days confirmed but missed PT: ', miss)
                        # print('________________________________________________')
                        # print('')

        x = x + 1
        test_count = test_count + 1
        ema_2_temp = ema_2_temp + 1
        if x == 6:
            x = 0
            ema_1_temp = ema_1_temp + 1
            ema_2_temp = ema_1_temp + 1
        if ema_1_temp == 4 and ema_2_temp == 9:
            #print("Done")
            print("Ticker",ticker)
            print("Timeframe = ", timeframe)
            print("Best rate = ", rate1, rate2)
            print("EMA = ", ema1best, ema2best)
            return


print("")
tickerList = ["TSLA", "NVDA","RIOT","MARA","DKNG", "NIO", "UPST", "PLTR",
              "GME", "AMC"]
timeframe = "10"

for tickernum in tickerList:
    print("Ticker: ", tickernum)
    runbacktest(tickernum, timeframe)





