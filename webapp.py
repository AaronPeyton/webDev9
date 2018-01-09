from flask import Flask, render_template, request, Markup, flash
import os, json, statistics

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)
with open('static/graduates.json') as graduate_data:
    data = json.load(graduate_data)
    majorList = {}
    for item in data:
        major = item['Major Information']['Major']


        majorList[major] = {}

        # basic info
        majorList[major]['Basic Information'] = ["Major Category: %s" % item["Major Information"]["Major Category"], "Rank by Median Earnings: %d" % item['Major Information']['Rank by Median Earnings'] , "Total number in major: %d" % item['Major Information']['Total Number in Major']]

        #demographics
        pWomen = round(float(item["Demographics"]["Women as Share of Total"])*100,2)
        pMen = round(100 - pWomen,2)
        majorList[major]['Demographic Information'] = ["Total Men: %d" % item["Demographics"]["Men"], "Total Women: %d" % item["Demographics"]["Women"] , "Percentage of Men: %s" % str(pMen) + "%", "Percentage of Women: %s" % str(pWomen) + "%" ]

        # earnings and job info
        pCJobs = round(float(item['Earnings']['College Jobs']) / float(item['Employment']['Employed']), 2)
        meanEarnings = int(item['Earnings']['Earnings Breakdown']['75th Percentile of Earnings']) + int(item['Earnings']['Earnings Breakdown']['25th Percentile of Earnings'])
        meanEarnings /= 2.0
        majorList[major]['Employment Information'] = [ "Total Employed: %d" % item['Employment']['Employed'], "Percent Employed in College Jobs: %s" % str(pCJobs) + "%", "Median Earnings: %d" % item['Earnings']['Earnings Breakdown']['Median Earnings'], "Mean Earnings: %d" % meanEarnings]


@app.route("/")
def render_main():
    return render_template('data_information.html')

@app.route("/major")
def render_major():
    if 'Major' in request.args:
        selected_major = request.args['Major']
        return render_template('majorInfo.html', response_options = get_majors(data), response_info = get_majorDetail(selected_major), response_major = selected_major)
    return render_template('majorInfo.html',response_options = get_majors(data))



@app.route("/division")
def render_division():
    # return render_template('divisionInfo.html')
    if 'Division' in request.args:
        selected_division = request.args['Division']
        return render_template('divisionInfo.html', response_options = get_divisions(data), response_info = get_divisionDetail(selected_division), response_division = selected_division)
    return render_template('divisionInfo.html',response_options = get_divisions(data))


def get_majors(data):
    lst = []
    for item in data:
        lst.append(item['Major Information']['Major'])
    lst.sort()
    string = ""
    for item in lst:
        string += Markup("<option value=\"" + item + "\">" + item + "</option>")
    return string

def get_majorDetail(major):
    major_detail = ''
    major_detail += Markup("<ul>")
    for item in majorList[major]:
        major_detail += Markup("<li><h4>%s</h4></li>" %item)
        major_detail += Markup("<ul>")
        for item2 in majorList[major][item]:
            major_detail += Markup("<li>%s</li>" %item2)
        major_detail += Markup("</ul>")
    major_detail += Markup("</ul>")
    return major_detail

def get_divisions(data):
    lst = ["Major Information", "Demographics", "Employment", "Earnings"]
    string = ''
    for item in lst:
        string += Markup("<option value=\"" + item + "\">" + item + "</option>")
    return string

def get_divisionDetail(department):
    divisionDetail = {"Major Information": getMajorInfoDict(), "Demographics": getDemographicInfoDict(), "Employment": getEmploymentInfoDict(), "Earnings": getEarningInfoDict()}
    dd = ''
    dd += Markup("<ul>")
    for item in divisionDetail[department]:
        dd += Markup("<li><h4>%s</h4></li>" %item)
        dd += Markup("<ul>")
        for item2 in divisionDetail[department][item]:
            dd+= Markup("<li>%s: %s</li>" %(item2, divisionDetail[department][item][item2]))
        dd += Markup("</ul>")
    return dd


def getMajorInfoDict():
    majorInformation = {"Division's Average Rank by Median Earnings": {}, "Average Total of Graduates in Division's Majors": {}}
    avgRank = {}
    avgTotal = {}
    for item in data:
        majorCategory = item["Major Information"]["Major Category"]
        if majorCategory not in avgRank:
            avgRank[majorCategory] = [item["Major Information"]["Rank by Median Earnings"]]
        else:
            avgRank[majorCategory].append(item["Major Information"]["Rank by Median Earnings"])
        if majorCategory not in avgTotal:
            avgTotal[majorCategory] = [item["Major Information"]["Total Number in Major"]]
        else:
            avgTotal[majorCategory].append(item["Major Information"]["Total Number in Major"])

    for item in avgRank:
        # print(item, avgRank[item])
        majorInformation["Division's Average Rank by Median Earnings"][item] = round(statistics.mean(avgRank[item]))
        # print(item, majorInformation["Average Rank by Median Earnings"][item])
    for item in avgTotal:
        # print(item, avgTotal[item])
        majorInformation["Average Total of Graduates in Division's Majors"][item] = round(statistics.mean(avgTotal[item]))
        # print(item, majorInformation["Average Totals in Majors"][item])
    return majorInformation

def getDemographicInfoDict():
    totalM = {}
    totalW = {}
    for item in data:
        majorCategory = item["Major Information"]["Major Category"]

        if majorCategory not in totalM:
            totalM[majorCategory] = item["Demographics"]["Men"]
        else:
            totalM[majorCategory] += item["Demographics"]["Men"]
        if majorCategory not in totalW:
            totalW[majorCategory] = item["Demographics"]["Women"]
        else:
            totalW[majorCategory] += item["Demographics"]["Women"]
        demoInfo = {"Total Male Graduates per Division" : totalM, "Total Female Graduates per Division" : totalW}
    return demoInfo

def getEmploymentInfoDict():
    totalFullTime = {}
    totalPartTime = {}
    totalUnemp = {}
    avgUnempRate = {}

    for item in data:
        majorCategory = item["Major Information"]["Major Category"]

        if majorCategory not in totalFullTime:
            totalFullTime[majorCategory] = item["Employment"]["Full Time"]
        else:
            totalFullTime[majorCategory] += item["Employment"]["Full Time"]
        if majorCategory not in totalPartTime:
            totalPartTime[majorCategory] = item["Employment"]["Part Time"]
        else:
            totalPartTime[majorCategory] += item["Employment"]["Part Time"]
        if majorCategory not in totalUnemp:
            totalUnemp[majorCategory] = item["Employment"]["Unemployed"]
        else:
            totalUnemp[majorCategory] += item["Employment"]["Unemployed"]
        if majorCategory not in avgUnempRate:
            avgUnempRate[majorCategory] = [item["Employment"]["Unemployment Rate"]]
        else:
            avgUnempRate[majorCategory].append(item["Employment"]["Unemployment Rate"])
    for item in avgUnempRate:
        avgUnempRate[item] = statistics.mean(avgUnempRate[item])
    employmentInfoDict = {"Total Graduates Working Full Time per Division" : totalFullTime, "Total Graduates Working Part Time per Division" : totalPartTime, "Total Unemployed Graduates per Division" : totalUnemp, "Average Unemployment Rate  of Graduates per Division" : avgUnempRate }
    return employmentInfoDict

def getEarningInfoDict():
    totalLWJ = {}
    totalNCJ = {}
    totalCJ = {}
    avgMedianEarnings = {}

    for item in data:
        majorCategory = item["Major Information"]["Major Category"]
        if majorCategory not in totalLWJ:
            totalLWJ[majorCategory] = item["Earnings"]["Low Wage Jobs"]
        else:
            totalLWJ[majorCategory] += item["Earnings"]["Low Wage Jobs"]
        if majorCategory not in totalNCJ:
            totalNCJ[majorCategory] = item["Earnings"]["College Jobs"]
        else:
            totalNCJ[majorCategory] += item["Earnings"]["College Jobs"]
        if majorCategory not in totalCJ:
            totalCJ[majorCategory] = item["Earnings"]["Non-College Jobs"]
        else:
            totalCJ[majorCategory] += item["Earnings"]["Non-College Jobs"]
        if majorCategory not in avgMedianEarnings:
            avgMedianEarnings[majorCategory] = [item["Earnings"]["Earnings Breakdown"]["Median Earnings"]]
        else:
            avgMedianEarnings[majorCategory].append(item["Earnings"]["Earnings Breakdown"]["Median Earnings"])
    for item in avgMedianEarnings:
        avgMedianEarnings[item] = round(statistics.mean(avgMedianEarnings[item]))
    earningsInfo = {"Total Graduates in Low Wage Jobs" : totalLWJ, "Total Graduates in Non-College Jobs" : totalNCJ, "Total Graduates in College Jobs" : totalCJ, "Graduate's Average Median Earnings": avgMedianEarnings}
    return earningsInfo


if __name__=="__main__":
    # set debug to false when publishing
    app.run(debug = True, port = 54321)
