  /**
   * 请求方法例子
   */
  // create: function () {
  //   var that = this;
  //       wx.request({
  //       url: Api.createCard() ,
  //       data: {
  //           "question":that.data.question,
  //           "color":that.data.color
  //       },
  //       method: 'POST',
  //       header: {
  //           'content-type': 'application/json',
  //       },
  //       success: function(res) {
  // 
  //           if(res.data.code=='200'){
  //               wx.showModal({
  //                   title: '创建成功',
  //                   content: res.data.msg,
  //                   showCancel: false,
  //                 })
  //                 setTimeout(function () {
  //                   wx.navigateBack({
  //                     delta: 1
  //                   })
  //                 }, 1000)                
  //           }else{
  //               wx.showModal({
  //                   title: '创建失败',
  //                   content: res.data.msg,
  //                   showCancel: false,
  //                 })
  //           }
  //       },
  //       fail: function() {},
  //       complete: function() {}
  //       })
  //   },


/**
 * 请求接口的例子
 */
// getCArdsMethods: function () {
//   var that = this;
//   wx.request({
//     url: Api.getSoup(),
//     method: 'GET',
//     header: {
//       'content-type': 'application/x-www-form-urlencoded',
//     },
//     success: function (res) {
//       if (res.data.code == "200") {
//         if (res.data.data.length >= 1) {
//           console.log(res.data.data)
//           that.setData({
//             soupsData: res.data.data,
//             index: 0,
//           })
//         } else {
//           wx.showModal({
//             title: '请求失败',
//             content: '没有数据~',
//             showCancel: false,
//           })
//         }
//       }
//     }
//   })

// },


// 根url
var HOST_URI = 'https://soup.hicaiji.com';
// 获取openid 
var GET_OPENID = '/wx/login?lg_code='
// 更新用户信息 
var UPDATE = '/update'
// 查看鸡汤 
var GET_Soup = '/soup'
// 收藏 需要openid 
var COLLECT = '/collect'
// 取消收藏 需要openid 
var COLLECT_DELETE = '/collect/delete'
// 查看我的收藏 需要openid 
var GET_MY_COLLECT = '/collects?openid='


// 获取openid_token 
function _getOpenid() {
  return HOST_URI + GET_OPENID;
}

// 更新用户信息
function _update() {
  return HOST_URI + UPDATE;
}

// 查看鸡汤
function _getSoup() {
  return HOST_URI + GET_Soup;
}

// 收藏 需要openid 
function _collect() {
  return HOST_URI + COLLECT;
}

// 收藏 需要openid 
function _collectDelete() {
  return HOST_URI + COLLECT_DELETE;
}

// 查看我的收藏 需要openid 
function _getMyCollect() {
  return HOST_URI + GET_MY_COLLECT;
}




module.exports = {
  getOpenid:_getOpenid,
  update:_update,
  getSoup: _getSoup,
  collect: _collect,
  collectDelete: _collectDelete,
  getMyCollect:_getMyCollect
};
