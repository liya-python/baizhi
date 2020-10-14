<template>
    <div>
        <Header></Header>
        <Banner></Banner>
        <Footer></Footer>
    </div>
</template>

<script>
    import Header from "./common/Header";
    import Footer from "./common/Footer";
    import Banner from "./common/Banner";

    export default {
        name: "Index",
        components:{
            Header:Header,
            Footer:Footer,
            Banner:Banner,
        }
    }
</script>

<style scoped>

</style>
