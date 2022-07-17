"""
        Here are located all necessary selectors for YELP parsing.
        All selectors are located in order how YELP changed its interface.
        Each time YELP updates selectors, fill this file in corresponding order.
        Do not forget to comment invalid selectors
"""
        

"""
Version 1
"""
#YELP_WELCOME = ".css-lf8rwb"
#NEXT_BUTTON = "#modal-portal-container > div:nth-child(2) > div > div > div > div > div.border-color--default__09f24__JbNoB > div > div > div.padding-t4__09f24__Y6aGL.padding-r4__09f24__PQlH_.padding-b4__09f24__q6U6q.padding-l4__09f24__XrHdl.border-color--default__09f24__NPAKY.text-align--left__09f24__ju_Ri > div > div:nth-child(2) > div > button" 
#RADIO_BUTTON = "#how_do_you_want_to_get_more_information--3"
#NAME_SELECTOR = "body > yelp-react-root > div:nth-child(1) > div.messenger-container__09f24__qt8O4 > div > div.messenger_right__09f24__fndbc.border--left__09f24__Lt8WF.border-color--default__09f24__JbNoB > div > div > div.u-flex__09f24__rt07y.u-flex-column__09f24__m6LIn.u-flex-item__09f24__YuSEF.border-color--default__09f24__JbNoB > div.messenger_right_top__09f24__ZxW58.u-padding-t3.u-padding-b3.border--bottom__09f24__Yl28T.border-color--default__09f24__JbNoB > div > div > div > div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.border-color--default__09f24__NPAKY > div.user-passport-info.border-color--default__09f24__NPAKY > span > a"
#SEND_BUTTON = "#modal-portal-container > div:nth-child(2) > div > div > div > div > div.border-color--default__09f24__JbNoB > div > div > div.padding-t4__09f24__Y6aGL.padding-r4__09f24__PQlH_.padding-b4__09f24__q6U6q.padding-l4__09f24__XrHdl.border-color--default__09f24__NPAKY.text-align--left__09f24__ju_Ri > div > div:nth-child(3) > button"
#SEND_BUTTON = "body > yelp-react-root > div:nth-child(1) > div.responsive.responsive-biz.border-color--default__09f24__NPAKY > div > div.biz-container-full-screen__09f24__fhNa6.border-color--default__09f24__NPAKY > div > div.responsive-biz.css-b95f0i.margin-b4__09f24__jfnOz.margin-sm-r0__09f24__WfNsG.margin-sm-b1__09f24__gvqD8.margin-md-r2__09f24__r7Qz5.border-color--default__09f24__NPAKY > div.css-s7x2v8.border-color--default__09f24__NPAKY > div.css-qe88f1.border-color--default__09f24__NPAKY > div > div > div.css-1dbbo0v.margin-t2__09f24__b0bxj.border-color--default__09f24__NPAKY > div.css-6z7iiq.margin-t2__09f24__b0bxj.border-color--default__09f24__NPAKY > button:nth-child(2)"
#ANSWER_BUTTON = "#modal-portal-container > div:nth-child(3) > div > div > div > div.border-color--default__09f24__NPAKY > div > div > div.css-40lu3n.padding-t3__09f24__TMrIW.padding-r3__09f24__eaF7p.padding-b4__09f24__q6U6q.padding-l3__09f24__IOjKY.border-color--default__09f24__NPAKY > div.css-1tocrcb.border-color--default__09f24__NPAKY > div.css-aurft1.border-color--default__09f24__NPAKY > div > button.css-o88s2i"
#EXPIRED_TIME_QUOTE = body > yelp-react-root > div > div.messenger-container__09f24__qt8O4 > div > div.messenger_right__09f24__fndbc.border--left__09f24__Lt8WF.border-color--default__09f24__JbNoB > div > div > div.u-flex__09f24__rt07y.u-flex-column__09f24__m6LIn.u-flex-item__09f24__YuSEF.border-color--default__09f24__JbNoB > div.project-description-container__09f24__zySxi.u-flex-item__09f24__YuSEF.messenger-right.border-color--default__09f24__JbNoB > div > div > div.messages-grouped-by-time-view_group_time-sent__09f24__lCCiu.border-color--default__09f24__NPAKY > p"

"""
Version 1.1
"""

#SEND_BUTTON = "div.margin-r3__09f24__ppHm0:nth-child(2) > button:nth-child(1)"
#LOGO = "#logo > a"


"""
Version 2 (new interface)
"""

#NEXT_BUTTON = "#modal-portal-container > div:nth-child(3) > div > div > div > div.border-color--default__09f24__NPAKY > div > div > div.css-40lu3n.padding-t3__09f24__TMrIW.padding-r3__09f24__eaF7p.padding-b4__09f24__q6U6q.padding-l3__09f24__IOjKY.border-color--default__09f24__NPAKY > div:nth-child(2) > div > button"
#RADIO_BUTTON = "#modal-portal-container > div:nth-child(3) > div > div > div > div.border-color--default__09f24__NPAKY > div > div > div.css-40lu3n.padding-t3__09f24__TMrIW.padding-r3__09f24__eaF7p.padding-b4__09f24__q6U6q.padding-l3__09f24__IOjKY.border-color--default__09f24__NPAKY > div:nth-child(1) > div:nth-child(4) > label > div"
NAME_SELECTOR = "span.fs-block > a:nth-child(1)"
OPTION_BUTTON = "div.margin-r3__09f24__ppHm0:nth-child(2) > button"
#NEED_MORE_INFO = "button.css-16nzldp:nth-child(2)" # SEND_BUTTON
#ANSWER_BUTTON = ".button--wide__09f24__dKiSe"
#READ_MORE_INBOX = "button.css-kma813:nth-child(2)"
SEE_FIRST = "div.css-1w7mn8k:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2)"
NEXT_ACTIVE = ".css-cednmx"
LOGO = "#logo"
EXPIRED_TIME_QUOTE = "div.css-19idom:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1)"
YELP_WELCOME = ".margin-b2__09f24__CEMjT"


"""
Version 2.1 (current)
"""

NEED_MORE_INFO = "button.css-16nzldp:nth-child(2)"
RADIO_BUTTON = "#radio-send_message"
NEXT_BUTTON = ".css-o88s2i"
MSG_AREA = ".textarea__09f24__jSO6c"
ANSWER_BUTTON = ".css-o88s2i"
NEARBY_DETAILS = "body > yelp-react-root > div:nth-child(1) > div.responsive.responsive-biz.border-color--default__09f24__NPAKY > div > div.biz-container__09f24__qO8rN.border-color--default__09f24__NPAKY > div > div.css-13c1rod.margin-b2__09f24__CEMjT.border-color--default__09f24__NPAKY > h1"
