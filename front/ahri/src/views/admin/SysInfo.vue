<template>
  <div id="sysinfo" class="sysinfo">
    <div class="bar">
      <router-link class="bg" to="/admin/sysinfo/bg">
        <span class="iconfont ahrisetting"></span>
        {{$t('lang.setting.bg')}}
      </router-link>
    </div>
    <div class="content">
      <router-view/>
    </div>
  </div>
</template>

<script>
export default {
  name: "sysinfo"
};
</script>

<style lang="scss" scoped>
#sysinfo {
  background: rgba(0, 0, 0, 0.3);
  height: 100%;
  padding: 15px;
  box-sizing: border-box;
  border-radius: 4px;
  position: relative;
  .bar {
    height: 40px;
    line-height: 40px;
    position: absolute;
    a {
      transition: 0.3s;
      &:hover {
        background: rgba(0, 0, 0, 0.4);
      }
    }
    .bg {
      position: absolute;
      top: 0;
      left: 0;
      display: inline-block;
      color: #fff;
      border: solid 1px #fff;
      border-bottom: none;
      height: 40px;
      width: 90px;
      border-radius: 8px 8px 0 0;
      text-align: center;
      text-decoration: none;
    }
  }
  .content {
    position: absolute;
    border: solid 1px #fff;
    bottom: 15px;
    top: 55px;
    left: 15px;
    right: 15px;
  }
}
</style>
