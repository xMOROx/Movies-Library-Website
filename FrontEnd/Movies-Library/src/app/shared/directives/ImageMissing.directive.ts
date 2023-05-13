import { Directive, ElementRef, HostListener, Renderer2 } from '@angular/core';

@Directive({
  selector: '[appImageMissing]'
})
export class ImageMissingDirective {

  constructor(private elementRef: ElementRef, private renderer: Renderer2) { }
  @HostListener('error')
  private onError() {
    this.renderer.removeAttribute(this.elementRef.nativeElement, 'srcset');
    this.renderer.setAttribute(this.elementRef.nativeElement, 'src', './assets/img/fallback.jpg');
  }
}
