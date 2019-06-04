<template>
  <div id="indexcate" class="indexcate">
    <p v-for="i in category" @click="goto(i.first)">{{i.name}}&nbsp;&nbsp;</p>
    <div v-if="category.length == 0">{{$t('lang.index.null')}}</div>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import loading from "@/assets/loading";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "indexcate",
  data() {
    return {
      category: []
    };
  },
  methods: {
    goto(id) {
      if (id !== "")
        this.$router.push({ path: "/read", query: { id: id.$oid } });
    }
  },
  mounted() {
    let load = loading(document.getElementById("indexcate"));
    let self = this;
    this.axios
      .get(url + "/api/index/indexcate")
      .then(response => {
        if (response.data.code === 200) {
          self.category = JSON.parse(response.data.data);
          document.getElementById("indexcate").removeChild(load);
        } else if (response.data.code === 400) {
          self.category = [];
          document.getElementById("indexcate").removeChild(load);
        } else {
          msg("未知错误..(from category get 500)", "#FF9966");
          console.log(response.data);
        }
      })
      .catch(response => {
        msg("未知错误..", "#FF9966");
        console.log(response);
      });
  }
};
</script>

<style lang="scss" scoped>
.indexcate {
  position: relative;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 30px;
  p {
    margin: 5px 15px;
    color: #777;
    font-weight: 700;
    cursor: pointer;
    text-decoration: underline;
    &:active {
      color: #000;
    }
  }
}
</style>
