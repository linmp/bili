//app.js
var Api = require('/utils/api.js');

App({
  onLaunch: function () {
    wx.getSystemInfo({
      success: e => {
        this.globalData.StatusBar = e.statusBarHeight;
        let capsule = wx.getMenuButtonBoundingClientRect();
        if (capsule) {
          this.globalData.Custom = capsule;
          this.globalData.CustomBar = capsule.bottom + capsule.top - e.statusBarHeight;
        } else {
          this.globalData.CustomBar = e.statusBarHeight + 50;
        }
      }
    })

    wx.login({
      success: res => {
        if (res.code) {
          wx.request({
            url: Api.getOpenid() + res.code,
            success: function (res) {
              if (res.data.openid) {
                var app = getApp();
                app.globalData.openid = res.data.openid;
                wx.hideLoading()

              }
            },
            fail: function () {
              wx.showModal({
                title: '提示',
                content: '加载失败,请检查网络状态,重新启动小程序',
                showCancel: false,
                success: function (res) {
                  wx.navigateBack({
                    delta: 1
                  })
                }
              })
            }
          })
        }
      }
    })

    // 进入页面加载的提示语
    wx.showLoading({
      title: "加载信息ing",
      mask: true

    })


    // 判断能否获取用户的信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: res => {
              this.globalData.userInfo = res.userInfo
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },

  globalData: {
    userInfo: null,
    openid: null,
    token: null
  }
})