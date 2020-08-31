var Api = require('../../../utils/api.js');
var startX, endX;
var moveFlag = true;// 判断执行滑动事件
const app = getApp();
Page({
  data: {
    index: 0,
    cardsData: [],
    page: 1,
    limit: 1,



  },


  /**
   * 监听加载数据
   */
  onLoad: function (options) {
    if (app.globalData.userInfo) {
      console.log("进入")
      updateuser(app.globalData.userInfo, app.globalData.openid)
    }
    this.getCArdsMethods()
  },



  /**
   * 获取卡片第一页数据
   */
  getCArdsMethods: function () {
    var that = this;
    wx.request({
      url: Api.getMyCollect() + app.globalData.openid,
      data: {
        page: 1,
        limit: that.data.limit
      },
      method: 'GET',
      header: {
        'content-type': 'application/x-www-form-urlencoded',
      },
      success: function (res) {
        if (res.data.code == "200") {
          if (res.data.data.length >= 1) {

            console.log(res.data.data)
            that.setData({
              cardsData: res.data.data,
              page: 2,
              index: 0,
            })
          } else {
            wx.showModal({
              title: '当前没有鸡汤',
              content: '快去添加你的第一碗鸡汤吧~',
              showCancel: false,
            })
            setTimeout(function () {
              wx.reLaunch({
                url: '/pages/soup/getSoup/index',
              })
            }, 1500)
          }
        } else {
          wx.showModal({
            title: '当前没有鸡汤',
            content: '快去添加你的第一碗鸡汤吧~',
            showCancel: false,
          })
          setTimeout(function () {
            wx.reLaunch({
              url: '/pages/soup/getSoup/index',
            })
          }, 1500)
        }
      }
    })

  },




  /**
   * 下一页的请求方法
   */
  nextCard: function () { 
    var that = this
    wx.request({
      url: Api.getMyCollect() + app.globalData.openid,
      data: {
        page: that.data.page,
        limit: that.data.limit
      },
      method: 'GET',
      header: {
        'content-type': 'application/x-www-form-urlencoded',
      },
      success: function (res) {
        if (res.data.code == '200') {
          console.log(res.data.code)

          if (res.data.data.length > 0) {
            that.setData({
              cardsData: that.data.cardsData.concat(res.data.data),
              page: that.data.page + 1
            })

          } else {
            console.log('没有数据')
          }
        } else {
          console.log('请求失败000')
        }
      },
    })
  },

  /**
   * 下一页
   */
  next: function () {
    this.setData({
      showNot: false
    })
    var that = this;
    console.log('当前数据是' + that.data.cardsData)
    this.nextCard()
  },

  /**
   * 删除收藏
   */
  collect: function (soup_id) {

    var that = this
    wx.request({
      url: Api.collectDelete(),
      data: {
        soup_id: soup_id,
        openid: app.globalData.openid,
      },
      header: {
          'content-type': 'application/json'
      },
      method: 'POST',
      success(res) {
        console.log(res)
        if (res.data.code == "200") {

          wx.showToast({
            title: '取消收藏成功',
          })

          that.getCArdsMethods()
        } else if (res.data.code == "4444") {
          wx.showToast({
            title: '请求过快',
            icon: 'none',
            duration: 3000
          })
        } else {
          wx.showToast({
            title: '操作失败',
            icon: 'none',
            duration: 3000
          })
        }
      }
    })
  },



  /**
   * 删除事件
   */
  askDelete: function (event) {
    console.log(event.currentTarget.dataset)
    var that = this
    wx.showModal({
      title: '目标id：' + event.currentTarget.dataset.id,
      content: '确定删除此条数据吗？',
      success(res) {
        if (res.confirm) {
          that.collect(event.currentTarget.dataset.id);

        }
      }
    })
  },





  /**
   * 下拉刷新事件, 数据同步
   */
  onPullDownRefresh: function () {
    wx.showToast({
      title: '正在同步数据',
      icon: 'loading'
    });
    this.onLoad()
    wx.stopPullDownRefresh()

  },

  //上滑
  onReachBottom: function () {
    this.next()
  },

})

function updateuser(user, openid) {
  var username = user.nickName;
  var avatar = user.avatarUrl;
  console.log("更新用户信息")
  wx.request({
    url: Api.update(),
    data: {
      openid: openid,
      username: username,
      avatar: avatar
    },
    header: {
      'content-type': 'application/json'
    },
    method: 'POST',
    success(res) {
      console.log(res.data);
    }
  })

}