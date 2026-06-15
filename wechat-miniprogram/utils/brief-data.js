const fallbackData = require("./issues");

const REMOTE_DATA_URL = "https://501807003.github.io/energy-brief-os/api/brief-data.json";

let cachedData = fallbackData;
let pendingRequest = null;

function isValidBriefData(data) {
  return Boolean(data && data.latestDate && data.issues && data.issues[data.latestDate]);
}

function fetchRemoteData() {
  if (pendingRequest) return pendingRequest;

  pendingRequest = new Promise((resolve) => {
    wx.request({
      url: `${REMOTE_DATA_URL}?t=${Date.now()}`,
      method: "GET",
      success(response) {
        if (response.statusCode >= 200 && response.statusCode < 300 && isValidBriefData(response.data)) {
          cachedData = response.data;
        }
        resolve(cachedData);
      },
      fail() {
        resolve(cachedData || fallbackData);
      },
      complete() {
        pendingRequest = null;
      }
    });
  });

  return pendingRequest;
}

function getBriefData() {
  return fetchRemoteData();
}

function getCachedBriefData() {
  return cachedData || fallbackData;
}

module.exports = {
  getBriefData,
  getCachedBriefData,
  fallbackData,
  REMOTE_DATA_URL
};
