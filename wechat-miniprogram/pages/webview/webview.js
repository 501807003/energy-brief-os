Page({
  data: {
    url: "",
    title: "原文"
  },

  onLoad(options) {
    const url = decodeURIComponent(options.url || "");
    const title = decodeURIComponent(options.title || "原文");
    this.setData({ url, title });
    wx.setNavigationBarTitle({ title });
  },

  copyLink() {
    if (!this.data.url) {
      wx.showToast({ title: "暂无链接", icon: "none" });
      return;
    }

    wx.setClipboardData({
      data: this.data.url,
      success: () => wx.showToast({ title: "链接已复制", icon: "success" })
    });
  }
});
