var Api = require('../../../utils/api.js');
var startX, endX;
var moveFlag = true;// 判断执行滑动事件
const app = getApp();

Page({
  data: {
    index: 0
  },

  /**
   * 查看说明
   */
  showModal(e) {
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
  },
  hideModal(e) {
    this.setData({
      modalName: null
    })
  },

  // 复制文字
  CopyData(e) {
    var that = this
    wx.setClipboardData({
      data: e.currentTarget.dataset.mdurl,
      success: res => {
        wx.showToast({
          title: '已复制',
          duration: 1000,
        })
      }
    })
  },


  /**
   * 监听加载数据
   */
  onLoad: function () {
    console.log("监听加载数据-获取卡片第一页数据")
    // 获取卡片第一页数据
    this.getCArdsMethods()
  },

  /**
   * 获取卡片第一页数据
   */
  getCArdsMethods: function () {
    var that = this;
    wx.request({
      url: Api.getSoup(),
      method: 'GET',
      header: {
        'content-type': 'application/x-www-form-urlencoded',
      },
      success: function (res) {
        if (res.data.code == "200") {
          if (res.data.data.length >= 1) {
            console.log(res.data.data)
            that.setData({
              soupsData: res.data.data,
              index: 0,
            })
          } else {
            wx.showModal({
              title: '请求失败',
              content: '没有数据~',
              showCancel: false,
            })
          }
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
      url: Api.getSoup(),
      method: 'GET',
      header: {
        'content-type': 'application/x-www-form-urlencoded',
      },
      success: function (res) {
        if (res.data.code == '200') {
          console.log(res.data.code)

          if (res.data.data.length > 0) {
            that.setData({
              soupsData: that.data.soupsData.concat(res.data.data),
              page: that.data.page + 1
            })
            that.next()

          } else {
            that.setData({
              page: 0,
              index: -1
            })
            console.log("调用函数")
            that.next()
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
    var that = this;
    console.log("当前数据", that.data.soupsData)
    if (that.data.index < that.data.soupsData.length - 1) {
      console.log('直接使用index' + (that.data.index + 1))
      that.setData({
        index: that.data.index + 1
      })
    } else {
      // 获取下一页分页的数据
      console.log(that.data.index + 1)
      console.log("最后一页 调用函数增加")
      this.nextCard()
    }
  },



  /**
   * 上一页
   */
  last: function () {
    this.setData({
      showNot: false
    })
    var that = this;
    if (that.data.index > 0) {
      console.log('直接使用前一个index' + (that.data.index - 1))
      that.setData({
        index: that.data.index - 1
      })
    } else {
      // 获取最后一页的数据 index 指向 length
      that.setData({
        index: that.data.soupsData.length
      })
      that.last()

    }
  },


  /**
   * 双击卡片的方法
   */
  collect: function () {
    var that = this

    var soup_id = this.data.soupsData[this.data.index].id
    wx.request({
      url: Api.collect(),
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
            title: '收藏成功',
          })
        } else if (res.data.code == "4444") {
          wx.showToast({
            title: '请求过快',
            icon: 'none',
            duration: 3000
          })
        } else {
          wx.showToast({
            title: '双击失败',
            icon: 'none',
            duration: 3000
          })
        }
      }
    })
  },


  // 单击双击
  mytap: function (e) {
    var curTime = e.timeStamp;
    var lastTime = this.data.lastTabDiffTime;
    if (lastTime > 0) {
      if (curTime - lastTime < 300) {
        console.log(e.timeStamp + '双击')

        this.collect();
      }
    }
    this.setData({
      lastTabDiffTime: curTime
    });
  },



  /**
   * 滑动
   */
  touchStart: function (e) {
    startX = e.touches[0].pageX; // 获取触摸时的原点
    console.log('开始')
    moveFlag = true;
  },

  
  // 触摸移动事件
  touchMove: function (e) {
    
    endX = e.touches[0].pageX; // 获取触摸时的原点
    if (moveFlag) {
      if (endX - startX > 15) {
        console.log("move right");
        this.last()
        moveFlag = false;

      }
      if (startX - endX > 15) {
        console.log("move left");
        // this.move2left();

        this.next();
        moveFlag = false;
      }
    }

  },


  // 触摸结束事件
  touchEnd: function (e) {
    moveFlag = true; // 回复滑动事件
    console.log('结束')
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

  // 分享
  onShareAppMessage: function () {
    return {
      title: this.data.soupsData[this.data.index].content,
      path: 'pages/soup/getSoup/index',
      imageUrl:this.imagePath
    }
  },

})