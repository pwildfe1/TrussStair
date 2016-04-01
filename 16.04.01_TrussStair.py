import rhinoscriptsyntax as rs
import math as m

def cantilieverProfile(pt,vec,depth,nParam,ratio):
    end = rs.PointAdd(pt,vec)
    top = rs.AddLine(pt,end)
    bot = rs.CopyObject(top,[0,0,-depth])
    param = rs.CurveParameter(bot,nParam)
    connectPt = rs.PointAdd(rs.EvaluateCurve(bot,param),[0,0,depth*ratio])
    botEnd = rs.PointAdd(rs.CurveEndPoint(bot),[0,0,depth*ratio])
    botStart = rs.CurveStartPoint(bot)
    rs.DeleteObject(bot)
    profile = rs.AddCurve([pt,botStart,connectPt,botEnd,end,pt],1)
    return profile

def arrayCrvPath(guide,length):
    steps = [] 
    profiles = []
    divPts = rs.DivideCurveLength(guide,1)
    for i in range(len(divPts)):
        param = rs.CurveClosestPoint(guide,divPts[i])
        tan = rs.CurveTangent(guide,param)
        norm = rs.VectorRotate(tan,90,[0,0,1])
        end = rs.PointAdd(divPts[i],norm*length)
        end = [end[0],end[1],divPts[i][2]]
        vec = rs.VectorCreate(end,divPts[i])
        nParam = abs(m.sin(i*m.pi/20))
        depthRatio = abs(m.sin(i*m.pi/20))
        if depthRatio>.9:
            depthRatio = .9
        profile = cantilieverProfile(divPts[i],vec,1,nParam,depthRatio)
        profiles.append(profile)
    for i in range(len(profiles)-1):
        newEnd = [divPts[i+1][0],divPts[i+1][1],divPts[i][2]]
        down = rs.VectorCreate(newEnd,divPts[i])
        endRun = rs.CopyObject(profiles[i+1],-down)
        steps.append(rs.AddLoftSrf([profiles[i+1],endRun]))
    return steps


def Main():
    guide = rs.GetObject("please select guide crv",rs.filter.curve)
    length = rs.GetReal("please enter desired width",5)
    steps = arrayCrvPath(guide,length)

Main()