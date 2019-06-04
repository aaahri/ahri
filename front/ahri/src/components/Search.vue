<template>
  <div class="search">
    <div class="logo"></div>
    <div class="name prohibit_copy">aaahri.com/</div>
    <div class="input">
      <input
        v-on:keyup.13="search"
        v-model:value="what"
        type="text"
        :placeholder="$t('lang.index.search')"
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "Search",
  data() {
    return {
      what: ""
    };
  },
  methods: {
    search() {
      this.$router.push({ path: "/search", query: { content: this.what } });
    }
  }
};
</script>

<style lang="scss" scoped>
.search {
  width: 600px;
  height: 80px;
  .logo {
    width: 60px;
    height: 60px;
    float: left;
    background: url("../assets/ahri.png") no-repeat center;
    background-size: 100%;
    cursor: pointer;
  }
  .name {
    width: 200px;
    height: 60px;
    float: left;
    font-size: 35px;
    line-height: 60px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    &:hover {
      color: #000;
    }
    &:active {
      color: #666;
    }
  }
  .input {
    width: 320px;
    height: 100px;
    float: left;
    line-height: 70px;
    input {
      width: 290px;
      height: 40px;
      font-size: 28px;
      outline: none;
      padding: 5px 0 0 15px;
      border: none;
      border-bottom: solid 2px rgba(0, 0, 0, 0.3);
      transition: 0.3s;
      color: #333;
      font-weight: 600;
      border-radius: 8px 8px 2px 2px;
      &:focus {
        border-top: solid 2px rgba(0, 0, 0, 0.2);
        border-left: solid 2px rgba(0, 0, 0, 0.2);
        border-right: solid 2px rgba(0, 0, 0, 0.2);
        border-bottom: solid 3px rgba(0, 0, 0, 0.3);
        width: 480px;
      }
    }
  }
}
</style>
