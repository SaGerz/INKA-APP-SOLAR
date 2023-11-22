const navbar = document.querySelector('.navbar')
console.log(navbar)
const sectionOne = document.querySelector('.white-bg')
const sectionTwo = document.querySelector('.section-welcome')

const sectionOneOptions = {
    rootMargin: "-200px 0px 0px 0px"
}
const sectionOneObserverWelcome = new IntersectionObserver(function (entries, sectionOneObserver) {
    entries.forEach(entry => {
       if(entry.isIntersecting){
          navbar.classList.add("navbar-light")
          navbar.classList.remove("navbar-dark") 
       } else {
          navbar.classList.add("navbar-dark")
          navbar.classList.remove("navbar-light")
       }
      // console.log(entry.target)
    })
}, sectionOneOptions)
sectionOneObserverWelcome.observe(sectionTwo)


const sectionOneObserver = new IntersectionObserver(function (entries, sectionOneObserver) {
    entries.forEach(entry => {
       if(entry.isIntersecting){
          navbar.classList.add("navbar-light")
          navbar.classList.remove("navbar-dark") 
       } else {
          navbar.classList.add("navbar-dark")
          navbar.classList.remove("navbar-light")
       }
      // console.log(entry.target)
    })
}, sectionOneOptions)

sectionOneObserver.observe(sectionOne)
